import copy
import uuid
from unittest.mock import MagicMock, patch
from cloudevents.http import CloudEvent
from wewu_less.models.send_notification_event import SendNotificationEvent
from wewu_less.schemas.send_notification_event import SendNotificationEventSchema
from wewu_less.handlers.notifier import wewu_notifier
from wewu_less.handlers.notifier import\
    publish_pubsub_with_delay, notify_first_admin, notify_second_admin\
    , notification_acked, wewu_notifier

from requests import Response

JOB_UUID = uuid.uuid4()
TEST_UUID = uuid.uuid4()

def _get_example_notify_task(
        Primary: bool = True,
) -> (CloudEvent):
    test_mail_1 = "abc@maileTutaj.com"
    test_mail_2 = "abc2@maileTutaj.com"
    escalation_number = 0 if Primary else 1
    request_json_object = {
        "jobId": JOB_UUID,
        "primaryAdmin": {
            "email": test_mail_1,
        },
        "secondaryAdmin": {
            "email": test_mail_2,
        },
        "ackTimeoutSecs": 60,
        "notificationId": None,
        "escalationNumber": escalation_number,
    }
    attributes = {
    "type": "com.example.sampletype1",
    "source": "https://example.com/event-producer",
    }
    return CloudEvent(attributes, request_json_object)

def test_wewu_notifier_primary_admin():
    event = _get_example_notify_task(True)
    expected_json_data = event.get_data().copy()
    expected_json_data["notificationId"] = TEST_UUID

    mock_queue = MagicMock()

    mongo_mock_find = MagicMock(return_value=expected_json_data)
    mongo_mock_insert = MagicMock()

    uuid_mock = MagicMock(return_value = TEST_UUID)

    mailjet_mock = MagicMock()
    response = Response()
    response.status_code = 200
    create_mock = MagicMock(return_value = response)
    create_mock.create.return_value = response
    mailjet_mock.return_value = create_mock
     
    
    with (
        patch('google.cloud.tasks_v2.CloudTasksClient.create_task', mock_queue),
        patch('wewu_less.repositories.notification.NotificationRepository.get_notification_by_id', mongo_mock_find),
        patch('wewu_less.repositories.notification.NotificationRepository.insert_notification', mongo_mock_insert),
        patch('uuid.uuid4', uuid_mock),
        patch('mailjet_rest.client.Client.__getattr__', mailjet_mock),
        ):
        wewu_notifier(copy.deepcopy(event))
    
    schema = SendNotificationEventSchema()
    expected_event = SendNotificationEvent(**schema.load(expected_json_data))
    mongo_mock_insert.assert_called_once_with(expected_event)
    mongo_mock_find.assert_not_called()
        
def test_wewu_notifier_secondary_admin():
    event = _get_example_notify_task(False)
    expected_json_data = event.get_data().copy()
    expected_json_data["notificationId"] = TEST_UUID

    mock_queue = MagicMock()

    mongo_mock_find = MagicMock(return_value=expected_json_data)
    mongo_mock_insert = MagicMock()

    uuid_mock = MagicMock(return_value = TEST_UUID)

    mailjet_mock = MagicMock()
    response = Response()
    response.status_code = 200
    create_mock = MagicMock(return_value = response)
    create_mock.create.return_value = response
    mailjet_mock.return_value = create_mock
     
    
    with (
        patch('google.cloud.tasks_v2.CloudTasksClient.create_task', mock_queue),
        patch('wewu_less.repositories.notification.NotificationRepository.get_notification_by_id', mongo_mock_find),
        patch('wewu_less.repositories.notification.NotificationRepository.insert_notification', mongo_mock_insert),
        patch('uuid.uuid4', uuid_mock),
        patch('mailjet_rest.client.Client.__getattr__', mailjet_mock),
        ):
        wewu_notifier(copy.deepcopy(event))
    
    schema = SendNotificationEventSchema()
    expected_event = SendNotificationEvent(**schema.load(expected_json_data))
    mongo_mock_insert.assert_called_once_with(expected_event)
    mongo_mock_find.assert_called_once_with(TEST_UUID)
