import datetime
from uuid import UUID

import flask

from wewu_less.logging import get_logger
from wewu_less.models.worker_monitor_task import WorkerMonitorTaskModel
from wewu_less.queues.publisher import publisher
from wewu_less.queues.worker_task_queue import WorkerTaskQueue
from wewu_less.repositories.database import mongo_client
from wewu_less.repositories.job import JobRepository
from wewu_less.utils import wewu_cloud_function

job_repository = JobRepository(mongo_client)
worker_task_queue = WorkerTaskQueue(publisher)
logger = get_logger()

WORKER_TIME_QUANT_SECS = 45 * 60


@wewu_cloud_function
def wewu_scheduler(_: flask.Request):
    try:
        expired_jobs = job_repository.get_expired_jobs()
    except Exception:
        logger.exception("Could not retrieve expired jobs")
        return {}, 500

    expiration_timestamp = (
        int(datetime.datetime.now(datetime.timezone.utc).timestamp())
        + WORKER_TIME_QUANT_SECS
    )
    worker_tasks = [
        WorkerMonitorTaskModel.from_job(job, expiration_timestamp)
        for job in expired_jobs
    ]

    logger.info("Scheduling worker tasks", task_count=len(worker_tasks))
    scheduled_worker_tasks = worker_task_queue.publish_tasks(worker_tasks)
    logger.info("Finished publishing messages", task_count=len(scheduled_worker_tasks))

    try:
        updated_job_ids: list[UUID] = list(
            map(lambda worker_task: worker_task.job_id, scheduled_worker_tasks)
        )
        if updated_job_ids:
            logger.info(
                "Updating expiration date of jobs", job_count=len(updated_job_ids)
            )
            job_repository.update_expiration_date(updated_job_ids, expiration_timestamp)
    except Exception:
        scheduled_ids = {task.job_id for task in scheduled_worker_tasks}
        logger.exception(
            "Can't save scheduling result to database - possible workers inconsistency",
            impacted_job_count=len(scheduled_ids),
            impacted_job_ids=scheduled_ids,
        )
        return {}, 500

    return {}, 200
