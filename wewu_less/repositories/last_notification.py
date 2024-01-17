from typing import Iterable, List

from pymongo import MongoClient, UpdateOne
from pymongo.collection import Collection

from wewu_less.logging import get_logger
from wewu_less.models.last_notification import LastNotification
from wewu_less.repositories.database import mongo_client as _mongo_client
from wewu_less.repositories.utils import sharding_step
from wewu_less.schemas.last_notification import LastNotificationSchema

last_notification_schema = LastNotificationSchema()
logger = get_logger()


class LastNotificationRepository:
    last_notifications: Collection

    def __init__(self, mongo_client: MongoClient = _mongo_client):
        self.last_notifications = mongo_client.notification_database.last_notifications

    def _mongo_to_model(self, mongo_last_notification: dict) -> LastNotification:
        parsed_last_notification = last_notification_schema.load(
            mongo_last_notification
        )
        return LastNotification(**parsed_last_notification)

    def get_last_notifications_by_shard(self, shard: int) -> Iterable[LastNotification]:
        aggregation_query = [*sharding_step(shard)]

        return map(
            self._mongo_to_model, self.last_notifications.aggregate(aggregation_query)
        )

    def upsert_last_notifications(self, last_notifications: List[LastNotification]):
        upsert_queries = [
            UpdateOne(
                {"jobId": str(last_notification.job_id)},
                {
                    "$set": {
                        "jobId": str(last_notification.job_id),
                        "lastProcessedPingTimestamp": last_notification.last_processed_ping_timestamp,
                    }
                },
                upsert=True,
            )
            for last_notification in last_notifications
        ]

        bulk_result = self.last_notifications.bulk_write(upsert_queries, ordered=False)
        bulk_errors = bulk_result.bulk_api_result.get("writeErrors", [])

        if bulk_errors:
            logger.error(
                "Error while upserting last notifications, will send notifications twice in the future",
                bulk_errors=bulk_errors,
            )
