import uuid
from random import Random
from typing import List, Optional
from unittest.mock import MagicMock, patch
from uuid import UUID

from pymongo.collection import Collection

from tests.integration.mongo import job_fixture
from wewu_less.handlers.buzzator import wewu_buzzator
from wewu_less.models.monitor_result import MonitorResult
from wewu_less.models.ping_result import PingResult
from wewu_less.models.send_notification_event import SendNotificationEvent
from wewu_less.schemas.monitor_result import MonitorResultSchema

TIMESTAMP_STEP = 10
RANDOM = Random("buzzator_test")

failures = [f for f in PingResult if f != PingResult.Success]
monitor_result_schema = MonitorResultSchema()


def generate_random_failure():
    failure_index = RANDOM.randint(0, len(failures) - 1)
    return failures[failure_index]


def ping_fixtures(
    job_id: UUID,
    pattern: List[bool],
    start_timestamp: int,
    monitor_result_collection: Optional[Collection] = None,
) -> List[MonitorResult]:
    mapped_pattern = [
        PingResult.Success if pattern_val else generate_random_failure()
        for pattern_val in pattern
    ]

    monitor_results = []
    for index, result in enumerate(mapped_pattern):
        monitor_results.append(
            MonitorResult(
                job_id=job_id,
                timestamp=(
                    start_timestamp + (len(mapped_pattern) - 1 - index) * TIMESTAMP_STEP
                ),
                result=result,
            )
        )

    if monitor_result_collection is not None:
        dumped_results = monitor_result_schema.dump(monitor_results, many=True)
        monitor_result_collection.insert_many(dumped_results)

    return monitor_results


def test_buzzator_alerting_on_one_failing_service(
    monitor_results_collection: Collection, jobs_collection: Collection
):
    notifications_interceptor = MagicMock()
    notifications_interceptor.side_effect = lambda x: x

    job_id = uuid.uuid4()

    job_fixture(
        job_id,
        jobs_collection,
        alerting_window_number_of_calls=10,
        alerting_window_calls_fail_count=6,
    )
    ping_fixtures(
        job_id,
        [
            False,
            True,
            True,
            True,
            True,
            True,
            False,
            False,
            True,
            True,
            False,
            False,
            False,
            False,
            False,
        ],
        0,
        monitor_result_collection=monitor_results_collection,
    )

    with patch(
        "wewu_less.queues.send_notification_event.SendNotificationEventQueue.publish_events",
        notifications_interceptor,
    ):
        wewu_buzzator({})

    notifications_interceptor.assert_called_once()
    assert len(notifications_interceptor.mock_calls[0].args[0]) == 1


def test_buzzator_alerting_on_two_services_one_healthy_one_failing(
    monitor_results_collection: Collection, jobs_collection: Collection
):
    notifications_interceptor = MagicMock()

    id1 = uuid.uuid4()
    id2 = uuid.uuid4()

    job_fixture(
        id1,
        jobs_collection,
        alerting_window_calls_fail_count=9,
        alerting_window_number_of_calls=10,
    )
    job_fixture(
        id2,
        jobs_collection,
        alerting_window_calls_fail_count=2,
        alerting_window_number_of_calls=10,
    )

    ping_fixtures(
        id1,
        [
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            True,
        ],
        0,
        monitor_result_collection=monitor_results_collection,
    )
    ping_fixtures(
        id2,
        [False, True, True, True, True, True, True, True, True, True, False],
        0,
        monitor_result_collection=monitor_results_collection,
    )

    with patch(
        "wewu_less.queues.send_notification_event.SendNotificationEventQueue.publish_events",
        notifications_interceptor,
    ):
        wewu_buzzator({})

    notifications_interceptor.assert_called_once()
    assert len(notifications_interceptor.mock_calls[0].args[0]) == 1

    notification_event: SendNotificationEvent = notifications_interceptor.mock_calls[
        0
    ].args[0][0]
    assert notification_event.job_id == id1
