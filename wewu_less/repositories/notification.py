from typing import Optional

from pymongo import MongoClient
from pymongo.collection import Collection

from wewu_less.logging import get_logger
from wewu_less.models.notification import NotificationEntity
from wewu_less.repositories.database import mongo_client as _mongo_client
from wewu_less.schemas.notification import NotificationSchema

notification_schema = NotificationSchema()
logger = get_logger()


class NotificationRepository:
    notification_events: Collection

    def __init__(self, mongo_client: MongoClient = _mongo_client):
        self.notification_events = mongo_client.notification_database.notifications

    def get_notification_by_id(
        self, notification_id: str
    ) -> Optional[NotificationEntity]:
        notifications = list(
            self.notification_events.find({"notificationId": notification_id})
        )
        count = len(notifications)
        if count > 1:
            logger.warning(
                "Found more than one notification with the same notification_id",
                notification_id=notification_id,
            )
        elif count == 0:
            return None
        entity = NotificationEntity(**(notification_schema.load(notifications[0])))
        return entity

    def insert_notification(self, notification: NotificationEntity) -> None:
        self.notification_events.insert_one(notification_schema.dump(notification))
