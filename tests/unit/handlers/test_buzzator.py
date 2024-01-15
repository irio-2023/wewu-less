import uuid
from random import Random
from typing import List
from unittest.mock import MagicMock, patch
from uuid import UUID

from wewu_less.handlers.buzzator import (
    _calculate_failing_jobs,
    _group_monitor_result_by_job_id,
)
from wewu_less.models.job import JobModel
from wewu_less.models.monitor_result import MonitorResult
from wewu_less.models.ping_result import PingResult

TIMESTAMP_STEP = 10
RANDOM = Random("buzzator_test")
failures = [f for f in PingResult if f != PingResult.Success]


def generate_random_failure():
    failure_index = RANDOM.randint(0, len(failures) - 1)
    return failures[failure_index]


def ping_fixtures(
    job_id: UUID, pattern: List[bool], start_timestamp: int
) -> List[MonitorResult]:
    mapped_pattern = [
        PingResult.Success if pattern_val else generate_random_failure()
        for pattern_val in pattern
    ]

    monitor_results = []
    for index, result in enumerate(mapped_pattern):
        monitor_results.append(
            MonitorResult(
                id=uuid.uuid4(),
                job_id=job_id,
                timestamp=(
                    start_timestamp + (len(mapped_pattern) - 1 - index) * TIMESTAMP_STEP
                ),
                result=result,
            )
        )

    return monitor_results


def job_fixture(
    job_id: UUID,
    alerting_window_number_of_calls: int,
    alerting_window_calls_fail_count: int,
) -> JobModel:
    return JobModel(
        job_id=job_id,
        alerting_window_number_of_calls=alerting_window_number_of_calls,
        alerting_window_calls_fail_count=alerting_window_calls_fail_count,
        primary_admin=None,
        secondary_admin=None,
        poll_frequency_secs=None,
        ack_timeout=None,
        is_cancelled=None,
        expiration_timestamp=None,
        service_url=None,
    )


def test_should_calculate_failing_jobs():
    job1_id = uuid.uuid4()
    job1_window, job1_failes = 5, 2
    job2_id = uuid.uuid4()
    job2_window, job2_failes = 5, 4
    job3_id = uuid.uuid4()
    job3_window, job_3_failes = 6, 6

    job_1 = job_fixture(job1_id, job1_window, job1_failes)
    job_2 = job_fixture(job2_id, job2_window, job2_failes)
    job_3 = job_fixture(job3_id, job3_window, job_3_failes)
    relevant_jobs = [job_1, job_2, job_3]

    job_1_results = ping_fixtures(
        job_1.job_id,
        [True, True, True, True, True, False, True, True, True, False, True, True],
        0,
    )
    job_2_results = ping_fixtures(
        job_2.job_id,
        [True, True, True, False, False, False, True, True, False, True],
        0,
    )
    job_3_results = ping_fixtures(
        job_3.job_id,
        [False, False, False, False, False, False, True, True, True],
        start_timestamp=100,
    )

    pings_mock = MagicMock()
    pings_mock.return_value = job_1_results + job_2_results + job_3_results

    with patch(
        "wewu_less.repositories.ping_result.PingResultRepository.get_pings_to_check",
        pings_mock,
    ):
        failing_jobs = _calculate_failing_jobs(relevant_jobs)
        assert failing_jobs == [(job_1.job_id, 60), (job_3.job_id, 180)]


def test_should_group_by_id():
    job1_id = uuid.uuid4()
    job1_results = ping_fixtures(
        job1_id,
        [True, True, True, True, True, False, True, True, True, False, True, True],
        0,
    )
    job2_id = uuid.uuid4()
    job_2_results = ping_fixtures(
        job2_id, [True, True, True, False, False, False, True, True, False, True], 0
    )
    job3_id = uuid.uuid4()
    job_3_results = ping_fixtures(
        job3_id,
        [False, False, False, False, False, False, True, True, True],
        start_timestamp=100,
    )

    grouped_results = [
        r
        for r in _group_monitor_result_by_job_id(
            job1_results + job_2_results + job_3_results
        )
    ]

    assert len(grouped_results) == 3
    assert len(grouped_results[0]) == len(job1_results)
    assert all([x.job_id == job1_id for x in grouped_results[0]])
    assert len(grouped_results[1]) == len(job_2_results)
    assert all([x.job_id == job2_id for x in grouped_results[1]])
    assert len(grouped_results[2]) == len(job_3_results)
    assert all([x.job_id == job3_id for x in grouped_results[2]])
