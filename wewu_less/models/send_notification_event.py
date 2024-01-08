import uuid
from dataclasses import dataclass

from wewu_less.models.service_admin import ServiceAdmin


@dataclass
class SendNotificationEvent:
    notification_id: uuid.UUID
    job_id: uuid.UUID
    primary_admin: ServiceAdmin
    secondary_admin: ServiceAdmin
    ack_timeout_secs: int
    escalation_number: int

    def __post_init__(self):
        if isinstance(self.primary_admin, dict):
            self.primary_admin = ServiceAdmin(**self.primary_admin)
        if isinstance(self.secondary_admin, dict):
            self.secondary_admin = ServiceAdmin(**self.secondary_admin)
