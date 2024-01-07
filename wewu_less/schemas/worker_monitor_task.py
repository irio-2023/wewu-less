from marshmallow import Schema, fields


class WorkerMonitorTaskSchema(Schema):
    job_id = fields.UUID(data_key="jobId")
    service_url = fields.Url(data_key="serviceUrl")
    poll_frequency_secs = fields.Integer(data_key="pollFrequencySecs")
    task_deadline_timestamp_secs = fields.Integer(data_key="taskDeadlineTimestampSecs")
