from marshmallow import Schema, fields

from wewu_less.schemas.service_admin import ServiceAdminSchema


class SendNotificationEventSchema(Schema):
    notification_id = fields.UUID(data_key="notificationId")
    job_id = fields.UUID(data_key="jobId")
    primary_admin = fields.Nested(ServiceAdminSchema, data_key="primaryAdmin")
    secondary_admin = fields.Nested(ServiceAdminSchema, data_key="secondaryAdmin")
    ack_timeout_secs = fields.Int(data_key="ackTimeoutSecs")
    escalation_number = fields.Int(data_key="escalationNumber", default=0)
