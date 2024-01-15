from marshmallow import Schema, fields


class LastNotificationSchema(Schema):
    job_id = fields.UUID(data_key="jobId", required=True)
    last_processed_ping_timestamp = fields.Integer(
        data_key="lastProcessedPingTimestamp", required=True
    )
