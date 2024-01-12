from dataclasses import dataclass, fields
from uuid import UUID

from wewu_less.models.service_admin import ServiceAdmin


@dataclass
class JobModel:
    job_id: UUID
    service_url: str
    primary_admin: ServiceAdmin
    secondary_admin: ServiceAdmin
    poll_frequency_secs: int
    alerting_window_size: int
    alerting_window_fail_count: int
    ack_timeout: int
    is_cancelled: bool
    expiration_timestamp: int | None = None

    def __post_init__(self):
        if isinstance(self.primary_admin, dict):
            self.primary_admin = ServiceAdmin(**self.primary_admin)
        if isinstance(self.secondary_admin, dict):
            self.secondary_admin = ServiceAdmin(**self.secondary_admin)

    @staticmethod
    def _filter_register_service_request(request: dict) -> dict:
        model_fields = {f.name for f in fields(JobModel)}
        return {k: v for k, v in request.items() if k in model_fields}

    @staticmethod
    def from_register_service_request(request: dict) -> "JobModel":
        request["expiration_timestamp"] = None
        request["is_cancelled"] = False
        filtered_request = JobModel._filter_register_service_request(request)

        return JobModel(**filtered_request)
