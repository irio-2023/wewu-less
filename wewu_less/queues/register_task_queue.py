import os

from google.cloud.pubsub import PublisherClient

from wewu_less.models.register_request import RegisterServiceRequest
from wewu_less.queues.abstract_queue import WewuQueue
from wewu_less.queues.publisher import publisher
from wewu_less.schemas.register_request import RegisterServiceRequestSchema

register_service_request_schema = RegisterServiceRequestSchema()

register_service_task_topic_name = "projects/{project_id}/topics/{topic}".format(
    project_id=os.environ["GOOGLE_CLOUD_PROJECT"],
    topic=os.environ["WEWU_REGISTER_TASK_QUEUE_TOPIC"],
)


class RegisterServiceTaskQueue(WewuQueue):
    def __init__(self, publisher_client: PublisherClient = publisher):
        super().__init__(publisher_client, register_service_task_topic_name)
        self._publisher_client = publisher_client

    def publish_tasks(self, messages: list[RegisterServiceRequest]):
        bytes_messages = [
            register_service_request_schema.dumps(m).encode() for m in messages
        ]
        super()._publish_messages(bytes_messages)
