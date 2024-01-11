from cloudevents.http import CloudEvent

from wewu_less.models.job import JobModel
from wewu_less.models.register_request import RegisterServiceRequest
from wewu_less.queues.register_task_queue import RegisterServiceTaskQueue
from wewu_less.repositories.job import JobRepository
from wewu_less.schemas.register_request import RegisterServiceRequestSchema
from wewu_less.utils import wewu_event_cloud_function, wewu_json_http_cloud_function

job_repository = JobRepository()
register_task_queue = RegisterServiceTaskQueue()
register_service_request_schema = RegisterServiceRequestSchema()


@wewu_json_http_cloud_function
def wewu_api_register_service(request_json: dict):
    parsed_body = register_service_request_schema.load(request_json)
    request = RegisterServiceRequest(**parsed_body)
    register_task_queue.publish_tasks([request])


@wewu_event_cloud_function
def wewu_api_copy_and_paste_inator(event: CloudEvent):
    parsed_body = register_service_request_schema.load(event.get_data())
    job = JobModel.from_register_service_request(parsed_body)

    # THIS IS ONLY FOR PURPOSE OF IRIO's SEMESTER PROJECT, REMOVE IN PRODUCTION
    # ADD MULTI REGIONAL SCHEDULING IN PRODUCTION MODE

    job_repository.save_new_job(job)
