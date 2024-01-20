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
        if isinstance(self.primaryAdmin, dict):
            self.primaryAdmin = ServiceAdmin(**self.primaryAdmin)
        if isinstance(self.secondaryAdmin, dict):
            self.secondaryAdmin = ServiceAdmin(**self.secondaryAdmin)
