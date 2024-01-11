import os

import pytest
from testcontainers.google import PubSubContainer
from testcontainers.mongodb import MongoDbContainer

from wewu_less.logging import get_logger

logger = get_logger()


def pytest_configure(config: pytest.Config):
    os.environ["GOOGLE_CLOUD_PROJECT"] = "wewu-less-it"
    os.environ["GOOGLE_WORKER_QUEUE_TOPIC"] = "wewu-worke"
    logger.info("Starting pytest configuration (docker containers)")
    mongo_container = MongoDbContainer()
    pubsub_container = PubSubContainer()

    mongo_container.start()
    pubsub_container.start()

    os.environ["MONGODB_URL"] = mongo_container.get_connection_url()

    def destroy_containers():
        mongo_container.stop()
        pubsub_container.stop()

        logger.info("Stopping session fixture containers")

    config.add_cleanup(destroy_containers)
