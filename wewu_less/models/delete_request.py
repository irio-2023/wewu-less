from dataclasses import dataclass
from uuid import UUID


@dataclass
class DeleteServiceRequest:
    job_id: UUID
