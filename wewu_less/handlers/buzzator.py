import time
from typing import Iterable, List, Tuple
from uuid import UUID

from wewu_less.logging import get_logger
from wewu_less.models.job import JobModel
from wewu_less.models.last_notification import LastNotification
from wewu_less.models.monitor_result import MonitorResult
from wewu_less.models.ping_result import PingResult
from wewu_less.models.send_notification_event import SendNotificationEvent
from wewu_less.queues.send_notification_event import SendNotificationEventQueue
from wewu_less.repositories.job import JobRepository
from wewu_less.repositories.last_notification import LastNotificationRepository
from wewu_less.repositories.ping_result import PingResultRepository
from wewu_less.utils import wewu_json_http_cloud_function

monitor_result_repository = PingResultRepository()
last_notification_repository = LastNotificationRepository()
send_notification_event_queue = SendNotificationEventQueue()
job_repository = JobRepository()
logger = get_logger()

CURRENT_SHARD = 1


def _group_monitor_result_by_job_id(
    monitor_results: Iterable[MonitorResult],
) -> Iterable[List[MonitorResult]]:
    is_first = True

    current_job_id: UUID
    chunk: List[MonitorResult] = []
    for result in monitor_results:
        if is_first:
            current_job_id = result.job_id
            is_first = False

        if current_job_id == result.job_id:
            chunk.append(result)
        else:
            yield chunk
            current_job_id = result.job_id
            chunk = [result]

    if chunk:
        yield chunk


def _calculate_failing_jobs(relevant_jobs: List[JobModel]) -> List[Tuple[UUID, int]]:
    pings_to_check = monitor_result_repository.get_pings_to_check(CURRENT_SHARD)
    job_window_map = {
        relevant_job.job_id: (
            relevant_job.alerting_window_number_of_calls,
            relevant_job.alerting_window_calls_fail_count,
        )
        for relevant_job in relevant_jobs
    }

    failing_jobs = []
    for chunk in _group_monitor_result_by_job_id(pings_to_check):
        job_id = chunk[0].job_id
        job_window_size, job_fail_count = job_window_map[chunk[0].job_id]

        if len(chunk) < job_window_size:
            # Too little jobs to find error
            continue

        # Initialize iteration variables
        error_timestamp = chunk[0].timestamp
        current_fail_count = 0
        for ping_result in chunk[:job_window_size]:
            if ping_result.result != PingResult.Success:
                current_fail_count += 1

        if current_fail_count >= job_fail_count:
            failing_jobs.append((job_id, error_timestamp))
            continue

        for index, ping_result in enumerate(chunk[job_window_size:]):
            error_timestamp = chunk[index + 1].timestamp
            current_fail_count -= chunk[index].result != PingResult.Success
            current_fail_count += ping_result.result != PingResult.Success

            if current_fail_count >= job_fail_count:
                failing_jobs.append((job_id, error_timestamp))
                continue

    return failing_jobs


def _publish_send_notification_events(
    failing_jobs: List[Tuple[UUID, int]], relevant_jobs: List[JobModel]
) -> List[Tuple[UUID, int]]:
    job_map = {job.job_id: job for job in relevant_jobs}
    last_timestamp_map = {
        job_id: last_processed_ping_timestamp
        for job_id, last_processed_ping_timestamp in failing_jobs
    }

    notification_events = []
    for job_id, _ in failing_jobs:
        job = job_map[job_id]

        notification_events.append(
            SendNotificationEvent(
                job_id=job_id,
                primary_admin=job.primary_admin,
                secondary_admin=job.secondary_admin,
                ack_timeout_secs=job.ack_timeout,
            )
        )

    if not notification_events:
        return []

    published_event = send_notification_event_queue.publish_events(notification_events)
    return [
        (event.job_id, last_timestamp_map[event.job_id]) for event in published_event
    ]


def _update_last_notification_entities(processed_failing_jobs: List[Tuple[UUID, int]]):
    last_notification_entities = [
        LastNotification(
            job_id=job_id, last_processed_ping_timestamp=last_ping_timestamp
        )
        for job_id, last_ping_timestamp in processed_failing_jobs
    ]

    last_notification_repository.upsert_last_notifications(last_notification_entities)


@wewu_json_http_cloud_function(accepts_body=False)
def wewu_buzzator():
    start_time = time.time()

    relevant_jobs = list(job_repository.get_jobs_by_shard(CURRENT_SHARD))
    failing_jobs = _calculate_failing_jobs(relevant_jobs)

    last_notification_timestamp_map = {
        last_notification.job_id: last_notification.last_processed_ping_timestamp
        for last_notification in last_notification_repository.get_last_notifications_by_shard(
            CURRENT_SHARD
        )
    }
    filtered_failing_jobs = [
        (job_id, last_ping_timestamp)
        for job_id, last_ping_timestamp in failing_jobs
        if last_notification_timestamp_map.get(job_id, 0) < last_ping_timestamp
    ]

    processed_failing_jobs = _publish_send_notification_events(
        filtered_failing_jobs, relevant_jobs
    )
    failed_count = len(filtered_failing_jobs) - len(processed_failing_jobs)
    if failed_count != 0:
        logger.error(
            "Failed publishing some of the notification events",
            failed_count=failed_count,
        )

    _update_last_notification_entities(processed_failing_jobs)

    end_time = time.time()

    logger.info("Buzzator execution finished", time_taken_secs=end_time - start_time)
