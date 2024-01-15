import os
from typing import List

from google.pubsub import PublisherClient

from wewu_less.models.delete_request import DeleteServiceRequest
from wewu_less.queues.abstract_queue import WewuQueue
from wewu_less.queues.publisher import publisher
from wewu_less.schemas.delete_request import DeleteServiceRequestSchema

delete_service_request_schema = DeleteServiceRequestSchema()
delete_service_task_topic_name = os.environ["WEWU_DELETE_TASK_QUEUE_TOPIC"]


class DeleteServiceTaskQueue(WewuQueue):
    def __init__(self, publisher_client: PublisherClient = publisher):
        super().__init__(publisher_client, delete_service_task_topic_name)

    def publish_tasks(
        self, messages: List[DeleteServiceRequest], should_throw: bool = False
    ) -> List[DeleteServiceRequest]:
        byte_messages = [
            (delete_service_request_schema.dumps(m).encode(), m) for m in messages
        ]
        return super()._publish_messages(byte_messages, should_throw=should_throw)
