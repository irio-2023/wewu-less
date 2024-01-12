import json
import uuid
from unittest.mock import MagicMock, patch

import flask

from tests.unit.utils import make_event_from_json_str, make_request_from_json_str
from wewu_less.handlers.entry import (
    wewu_api_copy_and_paste_inator,
    wewu_api_register_service,
)
from wewu_less.models.job import JobModel
from wewu_less.models.register_request import RegisterServiceRequest
from wewu_less.models.service_admin import ServiceAdmin

DETERMINISTIC_UUID = uuid.uuid4()


def _get_example_register_request(
    return_raw_json=False, include_job_id=False
) -> (flask.Request | str, RegisterServiceRequest):
    request_json_object = {
        "serviceURL": "https://google.com",
        "geoRegions": ["europe-central2-a"],
        "primaryAdmin": {"email": "abc@wp.pl"},
        "secondaryAdmin": {"phoneNumber": "123456789"},
        "pollFrequencySecs": 23,
        "alertingWindowSize": 52,
        "alertingWindowFailCount": 12,
        "ackTimeout": 36,
    }

    if include_job_id:
        request_json_object["jobId"] = str(DETERMINISTIC_UUID)

    primary_admin = ServiceAdmin(email="abc@wp.pl")
    second_admin = ServiceAdmin(phone_number="123456789")

    request_model = RegisterServiceRequest(
        job_id=DETERMINISTIC_UUID if include_job_id else None,
        service_url="https://google.com",
        geo_regions=["europe-central2-a"],
        primary_admin=primary_admin,
        secondary_admin=second_admin,
        poll_frequency_secs=23,
        alerting_window_size=52,
        alerting_window_fail_count=12,
        ack_timeout=36,
    )

    request_json = json.dumps(request_json_object)
    if return_raw_json:
        return request_json, request_model

    return make_request_from_json_str(request_json), request_model


def test_should_publish_message_after_register_request():
    publish_tasks_mock = MagicMock()
    uuid_mock = MagicMock()
    uuid_mock.return_value = DETERMINISTIC_UUID

    with (
        patch(
            "wewu_less.queues.register_task_queue.RegisterServiceTaskQueue.publish_tasks",
            publish_tasks_mock,
        ),
        patch("uuid.uuid4", uuid_mock),
    ):
        request, request_model = _get_example_register_request()
        register_response = wewu_api_register_service(request)
        setattr(request_model, "job_id", DETERMINISTIC_UUID)

    assert register_response == ({"jobId": str(DETERMINISTIC_UUID)}, 200)
    publish_tasks_mock.assert_called_once_with([request_model])


def test_copy_and_paste_inator_should_save_message_into_database():
    save_new_job_mock = MagicMock()

    raw_request: str
    request_model: RegisterServiceRequest
    raw_request, request_model = _get_example_register_request(
        return_raw_json=True, include_job_id=True
    )

    with (
        patch(
            "wewu_less.repositories.job.JobRepository.save_new_job", save_new_job_mock
        )
    ):
        wewu_api_copy_and_paste_inator(make_event_from_json_str(raw_request))

    job_model = JobModel(
        job_id=request_model.job_id,
        service_url=request_model.service_url,
        primary_admin=request_model.primary_admin,
        secondary_admin=request_model.secondary_admin,
        poll_frequency_secs=request_model.poll_frequency_secs,
        alerting_window_size=request_model.alerting_window_size,
        alerting_window_fail_count=request_model.alerting_window_fail_count,
        ack_timeout=request_model.ack_timeout,
        is_cancelled=False,
    )

    save_new_job_mock.assert_called_once_with(job_model)
