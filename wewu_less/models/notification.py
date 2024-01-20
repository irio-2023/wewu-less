from dataclasses import dataclass
from uuid import UUID

from wewu_less.models.service_admin import ServiceAdmin


@dataclass
class NotificationEntity:
    notification_id: UUID
    job_id: UUID
    primary_admin: ServiceAdmin
    secondary_admin: ServiceAdmin
    ack_timeout_secs: int
    acked: bool

    def __post_init__(self):
        if isinstance(self.primary_admin, dict):
            self.primaryAdmin = ServiceAdmin(**self.primary_admin)
        if isinstance(self.secondary_admin, dict):
            self.secondaryAdmin = ServiceAdmin(**self.secondary_admin)
