from dataclasses import dataclass
from uuid import UUID


@dataclass
class LastNotification:
    job_id: UUID
    last_processed_ping_timestamp: int
