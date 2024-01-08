from cloudevents.http import CloudEvent

from wewu_less.models.send_notification_event import SendNotificationEvent
from wewu_less.schemas.send_notification_event import SendNotificationEventSchema
from wewu_less.utils import wewu_cloud_function

send_notification_event_schema = SendNotificationEventSchema()


@wewu_cloud_function
def wewu_notifier(cloud_event: CloudEvent):
    notification_event_parsed = send_notification_event_schema.load(cloud_event.get_data())
    notification_event = SendNotificationEvent(**notification_event_parsed)

    if notification_event.escalation_number == 0:
        notify_first_admin(notification_event)
    else:
        notify_second_admin(notification_event)

def notify_first_admin(notification_event: SendNotificationEvent):
    pass

def notify_second_admin(notification_event: SendNotificationEvent):
    pass