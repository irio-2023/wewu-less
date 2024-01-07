from dataclasses import dataclass
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
    expiration_timestamp: int | None
