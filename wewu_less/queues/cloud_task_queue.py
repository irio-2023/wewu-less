import os

from google.cloud import tasks_v2

from wewu_less.logging import get_logger

queue_name = os.environ["WEWU_CLOUD_TASKS_QUEUE_NAME"]
queue_location = os.environ["WEWU_CLOUD_TASKS_QUEUE_REGION"]
queue_project = os.environ["WEWU_CLOUD_TASKS_QUEUE_PROJECT"]

default_queue_path = tasks_v2.CloudTasksClient.queue_path(
    queue_project, queue_location, queue_name
)

logger = get_logger()


class CloudTaskQueue:
    def __init__(
        self, client=tasks_v2.CloudTasksClient(), queue_path=default_queue_path
    ):
        self.client = client
        self.queue_path = queue_path

    def publish_task(self, url, payload, schedule_time):
        task = {
            "http_request": {
                "http_method": tasks_v2.HttpMethod.POST,
                "url": url,
                "body": payload.encode(),
                "headers": {"Content-Type": "application/json"},
            },
            "schedule_time": schedule_time,
        }
        task_request = {"parent": self.queue_path, "task": task}

        try:
            self.client.create_task(request=task_request)
        except Exception:
            logger.exception("Failed to schedule cloud task")
            raise
