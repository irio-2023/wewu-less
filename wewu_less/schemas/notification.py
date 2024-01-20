from marshmallow import Schema, fields

from wewu_less.schemas.service_admin import ServiceAdminSchema


class NotificationSchema(Schema):
    notification_id = fields.UUID(data_key="notificationId")
    job_id = fields.UUID(data_key="jobId")
    primary_admin = fields.Nested(
        ServiceAdminSchema, required=True, data_key="primaryAdmin"
    )
    secondary_admin = fields.Nested(
        ServiceAdminSchema, required=True, data_key="secondaryAdmin"
    )
    ack_timeout_secs = fields.Integer(data_key="ackTimeoutSecs")
    acked = fields.Boolean(data_key="acked")
