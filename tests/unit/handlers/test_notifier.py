import uuid
from unittest.mock import MagicMock, patch
import json

from cloudevents.http import CloudEvent
from requests import Response

from wewu_less.handlers.notifier import wewu_notifier
from wewu_less.models.notification import NotificationEntity
from tests.unit.utils import make_event_from_json_str

JOB_UUID = uuid.uuid4()
TEST_UUID = uuid.uuid4()


def _get_example_notify_task(
    Primary: bool = True,
) -> dict:
    test_mail_1 = "abc@maileTutaj.com"
    test_mail_2 = "abc2@maileTutaj.com"
    escalation_number = 0 if Primary else 1
    notification_id = None if Primary else str(TEST_UUID)
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


def test_wewu_notifier_primary_admin():
    event = _get_example_notify_task(True)

    notification = NotificationEntity(
        notificationId=TEST_UUID,
        jobId=JOB_UUID,
        primaryAdmin=event["primaryAdmin"],
        secondaryAdmin=event["secondaryAdmin"],
        ackTimeoutSecs=event["ackTimeoutSecs"],
        acked=False,
    )

    mock_queue = MagicMock()

    mongo_mock_find = MagicMock(return_value=notification)
    mongo_mock_insert = MagicMock()

    uuid_mock = MagicMock(return_value=TEST_UUID)

    mailjet_mock = MagicMock()
    response = Response()
    response.status_code = 200
    create_mock = MagicMock(return_value=response)
    create_mock.create.return_value = response
    mailjet_mock.return_value = create_mock

    with (
        patch("google.cloud.tasks_v2.CloudTasksClient.create_task", mock_queue),
        patch(
            "wewu_less.repositories.notification.NotificationRepository.get_notification_by_id",
            mongo_mock_find,
        ),
        patch(
            "wewu_less.repositories.notification.NotificationRepository.insert_notification",
            mongo_mock_insert,
        ),
        patch("uuid.uuid4", uuid_mock),
        patch("mailjet_rest.client.Client.__getattr__", mailjet_mock),
    ):
        event = make_event_from_json_str(json.dumps(event))
        wewu_notifier(event)

    mock_queue.assert_called_once()
    mongo_mock_insert.assert_called_once_with(notification)
    mongo_mock_find.assert_not_called()
    mailjet_mock.assert_called_once()


def test_wewu_notifier_secondary_admin_not_acked():
    event = _get_example_notify_task(False)

    notification = NotificationEntity(
        notificationId=TEST_UUID,
        jobId=JOB_UUID,
        primaryAdmin=event["primaryAdmin"],
        secondaryAdmin=event["secondaryAdmin"],
        ackTimeoutSecs=event["ackTimeoutSecs"],
        acked=False,
    )

    mock_queue = MagicMock()

    mongo_mock_find = MagicMock(return_value=notification)
    mongo_mock_insert = MagicMock()

    uuid_mock = MagicMock(return_value=TEST_UUID)

    mailjet_mock = MagicMock()
    response = Response()
    response.status_code = 200
    create_mock = MagicMock(return_value=response)
    create_mock.create.return_value = response
    mailjet_mock.return_value = create_mock

    with (
        patch("google.cloud.tasks_v2.CloudTasksClient.create_task", mock_queue),
        patch(
            "wewu_less.repositories.notification.NotificationRepository.get_notification_by_id",
            mongo_mock_find,
        ),
        patch(
            "wewu_less.repositories.notification.NotificationRepository.insert_notification",
            mongo_mock_insert,
        ),
        patch("uuid.uuid4", uuid_mock),
        patch("mailjet_rest.client.Client.__getattr__", mailjet_mock),
    ):
        event = make_event_from_json_str(json.dumps(event))
        wewu_notifier(event)

    mock_queue.assert_not_called()
    mongo_mock_insert.assert_not_called()
    mongo_mock_find.assert_called_once_with(TEST_UUID)
    mailjet_mock.assert_called_once()


def test_wewu_notifier_secondary_admin_acked():
    event = _get_example_notify_task(False)

    notification = NotificationEntity(
        notificationId=TEST_UUID,
        jobId=JOB_UUID,
        primaryAdmin=event["primaryAdmin"],
        secondaryAdmin=event["secondaryAdmin"],
        ackTimeoutSecs=event["ackTimeoutSecs"],
        acked=True,
    )

    mock_queue = MagicMock()

    mongo_mock_find = MagicMock(return_value=notification)
    mongo_mock_insert = MagicMock()

    uuid_mock = MagicMock(return_value=TEST_UUID)

    mailjet_mock = MagicMock()
    response = Response()
    response.status_code = 200
    create_mock = MagicMock(return_value=response)
    create_mock.create.return_value = response
    mailjet_mock.return_value = create_mock

    with (
        patch("google.cloud.tasks_v2.CloudTasksClient.create_task", mock_queue),
        patch(
            "wewu_less.repositories.notification.NotificationRepository.get_notification_by_id",
            mongo_mock_find,
        ),
        patch(
            "wewu_less.repositories.notification.NotificationRepository.insert_notification",
            mongo_mock_insert,
        ),
        patch("uuid.uuid4", uuid_mock),
        patch("mailjet_rest.client.Client.__getattr__", mailjet_mock),
    ):
        event = make_event_from_json_str(json.dumps(event))
        wewu_notifier(event)

    mock_queue.assert_not_called()
    mongo_mock_insert.assert_not_called()
    mongo_mock_find.assert_called_once_with(TEST_UUID)
    mailjet_mock.assert_not_called()
