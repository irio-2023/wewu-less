import os
from datetime import datetime

from google.cloud import tasks_v2

from wewu_less.logging import get_logger

service_account_email = os.environ["WEWU_SERVICE_ACCOUNT_EMAIL"]
pubsub_http_key = os.environ["WEWU_PUBSUB_HTTP_KEY"]

queue_name = os.environ["WEWU_CLOUD_TASKS_QUEUE_NAME"]
queue_location = os.environ["WEWU_CLOUD_TASKS_QUEUE_REGION"]
queue_project = os.environ["WEWU_CLOUD_TASKS_QUEUE_PROJECT"]

default_queue_path = tasks_v2.CloudTasksClient.queue_path(
    queue_project, queue_location, queue_name
)

logger = get_logger()

notify_topic = os.environ["WEWU_SEND_NOTIFICATION_EVENT_QUEUE_TOPIC"]


class CloudTaskQueue:
    def __init__(
        self, client=tasks_v2.CloudTasksClient(), queue_path=default_queue_path
    ):
        self.client = client
        self.queue_path = queue_path

    def publish_on_notifier_topic(self, payload: str, schedule_time: datetime):
        task = tasks_v2.Task(
            http_request=tasks_v2.HttpRequest(
                http_method=tasks_v2.HttpMethod.POST,
                url=f"https://pubsub.googleapis.com/v1/{notify_topic}:publish?key={pubsub_http_key}",
                body=payload,
            ),
            schedule_time=schedule_time,
        )
        logger.info("Publishing task to notifier topic", payload=payload)
        self.publish_task(task)

    def publish_task(self, task: tasks_v2.Task):
        try:
            self.client.create_task(request={"parent": self.queue_path, "task": task})
        except Exception:
            logger.exception("Failed to schedule cloud task")
            raise
