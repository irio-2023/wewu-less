import os
from typing import Iterable, List

from google.pubsub import PublisherClient

from wewu_less.models.send_notification_event import SendNotificationEvent
from wewu_less.queues.abstract_queue import WewuQueue
from wewu_less.queues.publisher import publisher
from wewu_less.schemas.send_notification_event import SendNotificationEventSchema

send_notification_event_schema = SendNotificationEventSchema()
send_notification_event_topic_name = os.environ[
    "WEWU_SEND_NOTIFICATION_EVENT_QUEUE_TOPIC"
]


class SendNotificationEventQueue(WewuQueue):
    def __init__(self, publisher_client: PublisherClient = publisher):
        super().__init__(publisher_client, send_notification_event_topic_name)

    def publish_events(
        self, messages: Iterable[SendNotificationEvent]
    ) -> List[SendNotificationEvent]:
        byte_messages = [
            (send_notification_event_schema.dumps(m).encode(), m) for m in messages
        ]
        return super()._publish_messages(byte_messages)
