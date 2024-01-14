from marshmallow import EXCLUDE, Schema, fields, validate

from wewu_less.models.ping_result import PingResult

possible_results = [r.value for r in PingResult]


class MonitorResultSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.UUID(required=True)
    job_id = fields.UUID(required=True, data_key="jobId")
    timestamp = fields.Integer(required=True)
    result = fields.String(required=True, validate=validate.OneOf(possible_results))
