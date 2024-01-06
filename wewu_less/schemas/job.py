from marshmallow import Schema, fields


class JobSchema(Schema):
    _id = fields.String()
    job_id = fields.UUID(data_key="jobId")
    service_url = fields.Url(data_key="serviceUrl")
    poll_frequency_secs = fields.Integer(data_key="pollFrequencySecs")
    alerting_window = fields.Integer(data_key="alertingWindow")
    alerting_window_fail_count = fields.Integer(data_key="alertingWindowFailCount")
    ack_timeout = fields.Integer(data_key="ackTimeout")
    is_cancelled = fields.Boolean(data_key="isCancelled")
    expiration_timestamp = fields.Integer(data_key="expirationTimestamp")
