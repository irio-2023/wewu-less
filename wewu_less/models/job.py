import uuid
from dataclasses import dataclass, fields
from uuid import UUID


@dataclass
class JobModel:
    job_id: UUID
    service_url: str
    poll_frequency_secs: int
    alerting_window: int
    alerting_window_fail_count: int
    ack_timeout: int
    is_cancelled: bool
    expiration_timestamp: int | None = None

    @staticmethod
    def _filter_register_service_request(request: dict) -> dict:
        model_fields = {f.name for f in fields(JobModel)}
        return {k: v for k, v in request if k in model_fields}

    @staticmethod
    def from_register_service_request(request: dict, job_id=uuid.uuid4()) -> "JobModel":
        request["job_id"] = job_id
        request["expiration_timestamp"] = None
        request["is_cancelled"] = False
        filtered_request = JobModel._filter_register_service_request(request)

        return JobModel(**filtered_request)
