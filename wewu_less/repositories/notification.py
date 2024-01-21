from typing import Optional

from pymongo import MongoClient
from pymongo.collection import Collection

from wewu_less.models.notification import NotificationEntity
from wewu_less.repositories.database import mongo_client as _mongo_client
from wewu_less.schemas.notification import NotificationSchema

notification_schema = NotificationSchema()


class NotificationRepository:
    ping_results: Collection

    def __init__(self, mongo_client: MongoClient = _mongo_client):
        self.ping_results = mongo_client.notification_database.notifications

    def get_notification_by_id(
        self, notification_id: str
    ) -> Optional[NotificationEntity]:
        return self.ping_results.find_one({"notification_id": notification_id})

    def insert_notification(self, notification: NotificationEntity) -> None:
        self.ping_results.insert_one(notification_schema.dump(notification))
