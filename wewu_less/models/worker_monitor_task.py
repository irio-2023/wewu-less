from dataclasses import dataclass
from uuid import UUID

from wewu_less.models.job import JobModel


@dataclass
class WorkerMonitorTaskModel:
    job_id: UUID
    service_url: str
    poll_frequency_secs: int
    task_deadline_timestamp_secs: int

    @staticmethod
    def from_job(
        job: JobModel, task_deadline_timestamp_secs: int
    ) -> "WorkerMonitorTaskModel":
        return WorkerMonitorTaskModel(
            job_id=job.job_id,
            service_url=job.service_url,
            poll_frequency_secs=job.poll_frequency_secs,
            task_deadline_timestamp_secs=task_deadline_timestamp_secs,
        )
