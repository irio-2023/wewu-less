from dataclasses import dataclass
from uuid import UUID

from wewu_less.models.ping_result import PingResult


@dataclass
class MonitorResult:
    id: UUID
    job_id: UUID
    timestamp: int
    result: PingResult

    def __post_init__(self):
        self.result = PingResult(self.result)
