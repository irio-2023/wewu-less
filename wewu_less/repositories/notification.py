
from pymongo import MongoClient
from pymongo.collection import Collection

from wewu_less.repositories.database import mongo_client as _mongo_client
from wewu_less.repositories.utils import sharding_step
from wewu_less.schemas.send_notification_event import SendNotificationEventSchema
from wewu_less.models.send_notification_event import SendNotificationEvent

send_notification_event_schema = SendNotificationEventSchema()

class NotificationRepository:
    ping_results: Collection

    def __init__(self, mongo_client: MongoClient = _mongo_client):
        self.ping_results = mongo_client.notification_database.notifications

    def get_notification_by_id(self, notification_id: str) -> SendNotificationEvent:
        self.ping_results.find_one({"notification_id": notification_id})
    
    def insert_notification(self, notification: SendNotificationEvent) -> None:
        self.ping_results.insert_one(send_notification_event_schema.dump(notification))
    
