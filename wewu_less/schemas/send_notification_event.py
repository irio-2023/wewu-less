from marshmallow import Schema, fields

from wewu_less.schemas.service_admin import ServiceAdminSchema


class SendNotificationEventSchema(Schema):
    notification_id = fields.UUID(
        required=False, default=None, allow_none=True, data_key="notificationId"
    )
    job_id = fields.UUID(required=True, data_key="jobId")
    primary_admin = fields.Nested(
        ServiceAdminSchema, required=True, data_key="primaryAdmin"
    )
    secondary_admin = fields.Nested(
        ServiceAdminSchema, required=True, data_key="secondaryAdmin"
    )
    ack_timeout_secs = fields.Integer(required=True, data_key="ackTimeoutSecs")
    escalation_number = fields.Integer(
        required=True, data_key="escalationNumber", default=0
    )
