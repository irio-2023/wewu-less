import os

from google.cloud.pubsub import PublisherClient

from wewu_less.models.register_request import RegisterServiceRequest
from wewu_less.queues.abstract_queue import WewuQueue
from wewu_less.queues.publisher import publisher
from wewu_less.schemas.register_request import RegisterServiceRequestSchema

register_service_request_schema = RegisterServiceRequestSchema()
register_service_task_topic_name = os.environ["WEWU_REGISTER_TASK_QUEUE_TOPIC"]


class RegisterServiceTaskQueue(WewuQueue):
    def __init__(self, publisher_client: PublisherClient = publisher):
        super().__init__(publisher_client, register_service_task_topic_name)

    def publish_tasks(
        self, messages: list[RegisterServiceRequest], should_throw: bool = False
    ) -> list[RegisterServiceRequest]:
        byte_messages = [
            (register_service_request_schema.dumps(m).encode(), m) for m in messages
        ]
        return super()._publish_messages(byte_messages, should_throw=should_throw)
