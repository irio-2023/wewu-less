from marshmallow import Schema, fields, validate

from wewu_less.models.geo_region import GeoRegion
from wewu_less.schemas.service_admin import ServiceAdminSchema

possible_regions = [r.value for r in GeoRegion]


class RegisterServiceRequestSchema(Schema):
    job_id = fields.UUID(required=True, data_key="jobId")
    service_url = fields.Url(required=True, data_key="serviceUrl")
    geo_regions = fields.List(
        cls_or_instance=fields.Str(validate=validate.OneOf(possible_regions)),
        required=True,
        data_key="geoRegions",
    )
    primary_admin = fields.Nested(
        ServiceAdminSchema, required=True, data_key="primaryAdmin"
    )
    secondary_admin = fields.Nested(
        ServiceAdminSchema, required=True, data_key="secondaryAdmin"
    )
    poll_frequency_secs = fields.Integer(required=True, data_key="pollFrequencySecs")
    alerting_window_number_of_calls = fields.Integer(
        required=True, data_key="alertingWindowNumberOfCalls"
    )
    alerting_window_calls_fail_count = fields.Integer(
        required=True, data_key="alertingWindowCallsFailCount"
    )
    ack_timeout = fields.Integer(required=True, data_key="ackTimeout")
