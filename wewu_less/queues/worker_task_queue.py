import os
from concurrent import futures

from google.cloud.pubsub import PublisherClient

from wewu_less.logging import WeWuLogger
from wewu_less.models.worker_monitor_task import WorkerMonitorTaskModel
from wewu_less.schemas.worker_monitor_task import WorkerMonitorTaskSchema

worker_task_topic_name = "projects/{project_id}/topics/{topic}".format(
    project_id=os.getenv("GOOGLE_CLOUD_PROJECT"),
    topic=os.getenv("GOOGLE_WORKER_QUEUE_TOPIC"),
)

worker_task_schema = WorkerMonitorTaskSchema()
logger = WeWuLogger()


class WorkerTaskQueue:
    publisher: PublisherClient

    def __init__(self, publisher: PublisherClient):
        self.publisher = publisher

    def publish_tasks(
        self, worker_tasks: list[WorkerMonitorTaskModel]
    ) -> list[WorkerMonitorTaskModel]:
        publish_futures = []
        publish_futures_mappings = []

        for worker_task in worker_tasks:
            message_str = worker_task_schema.dumps(worker_task)
            future = self.publisher.publish(
                worker_task_topic_name, str.encode(message_str)
            )
            publish_futures.append(future)
            publish_futures_mappings.append((future, worker_task))

        published_tasks = []
        futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)
        for future, task in publish_futures_mappings:
            if err := future.exception():
                logger.error(
                    "Can't publish worker monitor task", exc_info=err, worker_task=task
                )
            else:
                published_tasks.append(task)

        return published_tasks
