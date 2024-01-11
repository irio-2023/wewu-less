from abc import ABC
from concurrent import futures

from google.cloud.pubsub import PublisherClient

from wewu_less.logging import get_logger

logger = get_logger()


class WewuQueue(ABC):
    _publisher_client: PublisherClient
    _topic: str

    def __init__(self, publisher_client: PublisherClient, topic: str):
        self._topic = topic
        self._publisher_client = publisher_client

    def _publish_messages(self, messages: list[bytes]):
        publish_futures = []
        publish_futures_mappings = []

        for message_content in messages:
            future = self._publisher_client.publish(self._topic, message_content)

            publish_futures.append(future)
            publish_futures_mappings.append((future, message_content))

        published_tasks = []

        futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

        for future, task in publish_futures_mappings:
            if err := future.exception():
                raise err
            elif not future.cancelled():
                published_tasks.append(task)

        return published_tasks
