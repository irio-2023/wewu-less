from marshmallow import EXCLUDE, Schema, fields

from wewu_less.schemas.service_admin import ServiceAdminSchema


class JobSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    job_id = fields.UUID(data_key="jobId")
    service_url = fields.Url(data_key="serviceUrl")
    primary_admin = fields.Nested(
        ServiceAdminSchema, required=True, data_key="primaryAdmin"
    )
    secondary_admin = fields.Nested(
        ServiceAdminSchema, required=True, data_key="secondaryAdmin"
    )
    poll_frequency_secs = fields.Integer(data_key="pollFrequencySecs")
    alerting_window_number_of_calls = fields.Integer(
        data_key="alertingWindowNumberOfCalls"
    )
    alerting_window_calls_fail_count = fields.Integer(
        data_key="alertingWindowCallsFailCount"
    )
    ack_timeout = fields.Integer(data_key="ackTimeout")
    is_cancelled = fields.Boolean(data_key="isCancelled")
    expiration_timestamp = fields.Integer(
        data_key="expirationTimestamp", allow_none=True, default=None, required=False
    )
