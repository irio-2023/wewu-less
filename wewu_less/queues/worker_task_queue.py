import os

from google.cloud.pubsub import PublisherClient

from wewu_less.models.worker_monitor_task import WorkerMonitorTaskModel
from wewu_less.queues.abstract_queue import WewuQueue
from wewu_less.queues.publisher import publisher
from wewu_less.schemas.worker_monitor_task import WorkerMonitorTaskSchema

worker_task_schema = WorkerMonitorTaskSchema()
worker_task_topic_name = os.environ["WEWU_WORKER_QUEUE_TOPIC"]


class WorkerTaskQueue(WewuQueue):
    def __init__(self, publisher_client: PublisherClient = publisher):
        super().__init__(publisher_client, worker_task_topic_name)

    def publish_tasks(self, messages: list[WorkerMonitorTaskModel]):
        byte_messages = [worker_task_schema.dumps(m).encode() for m in messages]
        super()._publish_messages(byte_messages)
