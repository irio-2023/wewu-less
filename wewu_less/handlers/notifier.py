import dataclasses
import os
import uuid
from datetime import datetime, timedelta, timezone

from google.cloud import tasks_v2

from wewu_less.clients.email_client import EmailClient
from wewu_less.logging import get_logger
from wewu_less.models.notification import NotificationEntity
from wewu_less.models.send_notification_event import SendNotificationEvent
from wewu_less.models.service_admin import ServiceAdmin
from wewu_less.repositories.database import mongo_client
from wewu_less.repositories.notification import NotificationRepository
from wewu_less.schemas.notification import NotificationSchema
from wewu_less.schemas.send_notification_event import SendNotificationEventSchema
from wewu_less.utils import wewu_event_cloud_function

logger = get_logger()

notify_topic = os.environ["WEWU_SEND_NOTIFICATION_EVENT_QUEUE_TOPIC"]
queue_name = os.environ["WEWU_CLOUD_TASKS_QUEUE_NAME"]
queue_location = os.environ["WEWU_CLOUD_TASKS_QUEUE_REGION"]
queue_project = os.environ["WEWU_CLOUD_TASKS_QUEUE_PROJECT"]

queue_path = tasks_v2.CloudTasksClient.queue_path(
    queue_project, queue_location, queue_name
)

send_notification_event_schema = SendNotificationEventSchema()
notification_schema = NotificationSchema()

notification_repository = NotificationRepository(mongo_client)


@wewu_event_cloud_function
def wewu_notifier(event: dict):
    notification_event_parsed = send_notification_event_schema.load(event)
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
        "schedule_time": datetime.now(timezone.utc)
        + timedelta(seconds=notification_event.ack_timeout_secs),
    }
    task_request = {"parent": queue_path, "task": task}

    try:
        client.create_task(request=task_request)
    except Exception:
        logger.exception("Failed to schedule secondary admin notification")
        raise


def notification_acked(notification_id: uuid.UUID) -> bool:
    notification = notification_repository.get_notification_by_id(notification_id)
    if notification is None:
        logger.error("Notification not found", notification_id=notification_id)
        raise Exception
    return notification.acked


def add_notification(notification_event: SendNotificationEvent):
    notification = NotificationEntity(
        notificationId=notification_event.notification_id,
        jobId=notification_event.job_id,
        primaryAdmin=notification_event.primary_admin,
        secondaryAdmin=notification_event.secondary_admin,
        ackTimeoutSecs=notification_event.ack_timeout_secs,
        acked=False,
    )
    notification_repository.insert_notification(notification)


def notify_first_admin(notification_event: SendNotificationEvent):
    notification_event.notification_id = uuid.uuid4()
    second_notification_event = dataclasses.replace(
        notification_event, escalation_number=1
    )
    add_notification(notification_event)
    publish_pubsub_with_delay(second_notification_event)
    send_to_admin(notification_event, notification_event.primary_admin)


def notify_second_admin(notification_event: SendNotificationEvent):
    if notification_acked(notification_event.notification_id):
        return
    send_to_admin(notification_event, notification_event.secondary_admin)


def send_to_admin(notification_event: SendNotificationEvent, admin: ServiceAdmin):
    if admin.email:
        logger.info(
            "Sending email to admin",
            mail=admin.email,
            notification_id=notification_event.notification_id,
        )
        send_email(notification_event, admin.email)
    else:
        send_sms(notification_event, admin.phone_number)


def send_email(notification_event: SendNotificationEvent, email: str):
    mail_client = EmailClient()
    mail_client.send_notification(notification_event, email)


def send_sms(notification_event: SendNotificationEvent, phone_number: str):
    pass
