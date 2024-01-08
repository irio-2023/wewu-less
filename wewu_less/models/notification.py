from dataclasses import dataclass
from uuid import UUID

from wewu_less.models.service_admin import ServiceAdmin


@dataclass
class NotificationEntity:
    notificationId: UUID
    jobId: UUID
    primaryAdmin: ServiceAdmin
    secondaryAdmin: ServiceAdmin
    ackTimeoutSecs: int
    acked: bool

    def __post_init__(self):
        if isinstance(self.primary_admin, dict):
            self.primary_admin = ServiceAdmin(**self.primary_admin)
        if isinstance(self.secondary_admin, dict):
            self.secondary_admin = ServiceAdmin(**self.secondary_admin)
