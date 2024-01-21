import uuid
from unittest.mock import MagicMock, patch

from pymongo.collection import Collection

from tests.integration.utils import create_event_mock
from wewu_less.handlers.notifier import wewu_notifier

TEST_UUID = uuid.uuid4()
JOB_UUID = uuid.uuid4()


def _get_example_notify_task(primary: bool):
    test_mail_1 = "abc@maileTutaj.com"
    test_mail_2 = "abc2@maileTutaj.com"
    escalation_number = 0 if primary else 1
    notification_id = None if primary else str(TEST_UUID)
    request_json_object = {
        "jobId": str(JOB_UUID),
        "primaryAdmin": {
            "email": test_mail_1,
        },
        "secondaryAdmin": {
            "email": test_mail_2,
        },
        "ackTimeoutSecs": 60,
        "notificationId": notification_id,
        "escalationNumber": escalation_number,
    }
    return request_json_object


def test_notifier_should_insert_notification(notification_collection: Collection):
    event = _get_example_notify_task(True)

    mock_queue = MagicMock(autospec=True)
    mail_mock = MagicMock(autospec=True)

    uuid_mock = MagicMock(return_value=TEST_UUID)

    with (
        patch("wewu_less.handlers.notifier.uuid.uuid4", uuid_mock),
        patch(
            "wewu_less.clients.email_client.EmailClient.send_notification", mail_mock
        ),
        patch(
            "wewu_less.queues.cloud_task_queue.CloudTaskQueue.publish_on_notifier_topic",
            mock_queue,
        ),
    ):
        wewu_notifier(create_event_mock(event))
        db_notifications = list(
            notification_collection.find({"notificationId": str(TEST_UUID)})
        )
        assert len(db_notifications) == 1
        assert db_notifications[0]["notificationId"] == str(TEST_UUID)
        print(db_notifications[0])
        event["notificationId"] = str(TEST_UUID)
        event["escalationNumber"] = 1
        wewu_notifier(create_event_mock(event))
