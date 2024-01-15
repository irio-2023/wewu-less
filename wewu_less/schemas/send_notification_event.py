from marshmallow import Schema, fields

from wewu_less.schemas.service_admin import ServiceAdminSchema


class SendNotificationEventSchema(Schema):
    job_id = fields.UUID(data_key="jobId", required=True)
    primary_admin = fields.Nested(
        ServiceAdminSchema, required=True, data_key="primaryAdmin"
    )
    secondary_admin = fields.Nested(
        ServiceAdminSchema, required=True, data_key="secondaryAdmin"
    )
    ack_timeout_secs = fields.Integer(required=True, data_key="ackTimeoutSecs")
