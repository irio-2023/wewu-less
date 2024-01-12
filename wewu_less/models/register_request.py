from dataclasses import dataclass
from typing import List
from uuid import UUID

from marshmallow.fields import URL

from wewu_less.models.geo_region import GeoRegion
from wewu_less.models.service_admin import ServiceAdmin


@dataclass
class RegisterServiceRequest:
    service_url: URL
    geo_regions: List[GeoRegion]
    primary_admin: ServiceAdmin
    secondary_admin: ServiceAdmin
    poll_frequency_secs: int
    alerting_window_size: int
    alerting_window_fail_count: int
    ack_timeout: int
    job_id: UUID | None = None

    def __post_init__(self):
        self.geo_regions = [GeoRegion(g) for g in self.geo_regions]
        if isinstance(self.primary_admin, dict):
            self.primary_admin = ServiceAdmin(**self.primary_admin)
        if isinstance(self.secondary_admin, dict):
            self.secondary_admin = ServiceAdmin(**self.secondary_admin)
