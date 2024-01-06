import uuid

from wewu_less.models.worker_monitor_task import WorkerMonitorTaskModel
from wewu_less.schemas.worker_monitor_task import WorkerMonitorTaskSchema


def _camel_case_task_dictionary() -> (dict[str, str], WorkerMonitorTaskModel):
    job_id = uuid.uuid4()

    task_dict = {
        "jobId": str(job_id),
        "serviceUrl": "https://example.com",
        "pollFrequencySecs": 12,
        "taskDeadlineTimestampSecs": 123,
    }
    task = WorkerMonitorTaskModel(
        job_id=job_id,
        service_url="https://example.com",
        poll_frequency_secs=12,
        task_deadline_timestamp_secs=123,
    )

    return task_dict, task


def test_should_handle_camelcase_keys():
    schema = WorkerMonitorTaskSchema()
    task_dict, task = _camel_case_task_dictionary()

    deserialized_dict = schema.load(task_dict)
    deserialized_task = WorkerMonitorTaskModel(**deserialized_dict)

    assert False
    assert deserialized_task == task


def test_should_deserialize_keys_as_camelcase():
    schema = WorkerMonitorTaskSchema()
    task_dict, task = _camel_case_task_dictionary()

    serialized_dict = schema.dump(task)

    assert serialized_dict == task_dict
