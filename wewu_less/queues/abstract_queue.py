from abc import ABC
from concurrent import futures
from typing import TypeVar

from google.cloud.pubsub import PublisherClient

from wewu_less.logging import get_logger

logger = get_logger()


class WewuQueue(ABC):
    T = TypeVar("T")
    _publisher_client: PublisherClient
    _topic: str

    def __init__(self, publisher_client: PublisherClient, topic: str):
        self._topic = topic
        self._publisher_client = publisher_client

    def _publish_messages(self, messages: list[tuple[bytes, T]]) -> list[T]:
        publish_futures = []
        publish_futures_mappings = []

        for message_content, original_object in messages:
            future = self._publisher_client.publish(self._topic, message_content)

            publish_futures.append(future)
            publish_futures_mappings.append((future, original_object))

        published_tasks = []

        futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

        for future, task in publish_futures_mappings:
            if err := future.exception():
                logger.error(
                    "Got exception while publishing task to the queue",
                    topic=self._topic,
                    exc_info=err,
                )
            elif not future.cancelled():
                published_tasks.append(task)

        return published_tasks
