import dataclasses
import os
import uuid
from datetime import datetime, timedelta

from cloudevents.http import CloudEvent
from google.cloud import tasks_v2
from mailjet_rest import Client

from wewu_less.logging import get_logger
from wewu_less.models.notification import NotificationEntity
from wewu_less.models.send_notification_event import SendNotificationEvent
from wewu_less.models.service_admin import ServiceAdmin
from wewu_less.repositories.database import mongo_client
from wewu_less.schemas.send_notification_event import SendNotificationEventSchema
from wewu_less.utils import wewu_cloud_function
from wewu_less.repositories.notification import NotificationRepository

logger = get_logger()

notify_topic = os.environ["WEWU_SEND_NOTIFICATION_EVENT_QUEUE_TOPIC"]
notification_url = os.environ["NOTIFICATION_URL"]
service_mail = os.environ["SERVICE_MAIL"]
mail_api_key = os.environ["MAIL_API_KEY"]
mail_api_secret = os.environ["MAIL_API_SECRET"]
queue_name = os.environ["WEWU_CLOUD_TASKS_QUEUE_NAME"]
queue_location = os.environ["WEWU_CLOUD_TASKS_QUEUE_REGION"]
queue_project = os.environ["WEWU_CLOUD_TASKS_QUEUE_PROJECT"]

queue_path = tasks_v2.CloudTasksClient.queue_path(
    queue_project, queue_location, queue_name
)

send_notification_event_schema = SendNotificationEventSchema()

notification_repository = NotificationRepository(mongo_client)

@wewu_cloud_function
def wewu_notifier(cloud_event: CloudEvent):
    notification_event_parsed = send_notification_event_schema.load(
        cloud_event.get_data()
    )
    notification_event = SendNotificationEvent(**notification_event_parsed)
    if notification_event.escalation_number == 0:
        notify_first_admin(notification_event)
    else:
        notify_second_admin(notification_event)


def publish_pubsub_with_delay(notification_event: SendNotificationEvent):
    client = tasks_v2.CloudTasksClient()

    url = f"https://pubsub.googleapis.com/v1/{notify_topic}:publish"

    payload = send_notification_event_schema.dumps(notification_event)

    task = {
        "http_request": {
            "http_method": tasks_v2.HttpMethod.POST,
            "url": url,
            "body": payload.encode(),
            "headers": {"Content-Type": "application/json"},
        },
        "schedule_time": (
            datetime.utcnow() + timedelta(seconds=notification_event.ack_timeout_secs)
        ).isoformat()
        + "Z",
    }
    task_request = {"parent": queue_path, "task": task}

    try:
        client.create_task(request=task_request)
    except Exception:
        logger.exception(
            f"Failed to schedule secondary admin notification"
            f"(notificationId: {notification_event.notification_id})"
        )
        raise


def notification_acked(notification_id: uuid.UUID) -> bool:
    notification_data = notification_repository.get_notification_by_id(notification_id) 
    notification = NotificationEntity(**notification_data)
    return notification.acked


def notify_first_admin(notification_event: SendNotificationEvent):
    notification_event.notification_id = uuid.uuid4()
    second_notification_event = dataclasses.replace(
        notification_event, escalation_number=1
    )
    publish_pubsub_with_delay(second_notification_event)
    notification_repository.insert_notification(notification_event)
    send_to_admin(notification_event, notification_event.primary_admin)


def notify_second_admin(notification_event: SendNotificationEvent):
    if notification_acked(notification_event.notification_id):
        return
    send_to_admin(notification_event, notification_event.secondary_admin)


def send_to_admin(notification_event: SendNotificationEvent, admin: ServiceAdmin):
    if admin.email:
        logger.info(
            f"Sending email to {admin.email} (notificationId: {notification_event.notification_id})"
        )
        send_email(notification_event, admin.email)
    else:
        send_sms(notification_event, admin.phone_number)


def send_email(notification_event: SendNotificationEvent, email: str):
    try:
        mailjet = Client(auth=(mail_api_key, mail_api_secret))
        url = f"{notification_url}?notificationId={notification_event.notification_id}"
        data = {
            "FromEmail": service_mail,
            "FromName": "Wewu Alerter",
            "Subject": "[WEWU] Service fail detected",
            "Text-part": f"Fail for job {notification_event.job_id} detected.\n ACK: {url}",
            "Recipients": [{"Email": email}],
        }
        result = mailjet.send.create(data=data)
        if result.status_code != 200:
            raise Exception(result.status_code, result.text)
    except Exception:
        logger.exception(
            "Failed to send mail",
            mail=email,
            notification_id=notification_event.notification_id,
        )
        raise


def send_sms(notification_event: SendNotificationEvent, phone_number: str):
    pass
