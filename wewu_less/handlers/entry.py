import uuid

from wewu_less.logging import get_logger
from wewu_less.models.delete_request import DeleteServiceRequest
from wewu_less.models.job import JobModel
from wewu_less.models.register_request import RegisterServiceRequest
from wewu_less.queues.delete_task_queue import DeleteServiceTaskQueue
from wewu_less.queues.register_task_queue import RegisterServiceTaskQueue
from wewu_less.repositories.job import JobRepository
from wewu_less.schemas.delete_request import DeleteServiceRequestSchema
from wewu_less.schemas.register_request import RegisterServiceRequestSchema
from wewu_less.utils import wewu_event_cloud_function, wewu_json_http_cloud_function

logger = get_logger()

job_repository = JobRepository()
register_task_queue = RegisterServiceTaskQueue()
delete_task_queue = DeleteServiceTaskQueue()
register_service_request_schema_without_id = RegisterServiceRequestSchema(
    exclude=("job_id",)
)
register_service_request_schema = RegisterServiceRequestSchema()
delete_service_request_schema = DeleteServiceRequestSchema()


@wewu_json_http_cloud_function(accepts_body=True)
def wewu_api_register_service(request_json: dict):
    parsed_body = register_service_request_schema_without_id.load(request_json)

    job_id = uuid.uuid4()
    parsed_body["job_id"] = job_id

    request = RegisterServiceRequest(**parsed_body)
    register_task_queue.publish_tasks([request], should_throw=True)

    logger.info(
        "Successfully pushed register service request onto Pub/Sub", job_id=job_id
    )

    return {"jobId": str(job_id)}, 200


@wewu_json_http_cloud_function(accepts_body=True)
def wewu_api_delete_service(request_json: dict):
    parsed_body = delete_service_request_schema.load(request_json)

    request = DeleteServiceRequest(**parsed_body)
    delete_task_queue.publish_tasks([request], should_throw=True)

    logger.info(
        "Successfully pushed delete service request onto Pub/Sub", job_id=request.job_id
    )

    return {}, 200


@wewu_event_cloud_function
def wewu_api_copy_and_paste_inator(event: dict):
    parsed_body = register_service_request_schema.load(event)
    job = JobModel.from_register_service_request(parsed_body)

    # THIS IS ONLY FOR PURPOSE OF IRIO's SEMESTER PROJECT, REMOVE IN PRODUCTION
    # ADD MULTI REGIONAL SCHEDULING IN PRODUCTION MODE

    job_repository.save_new_job(job)
    logger.info("Successfully added job to the database", job_id=job.job_id)


@wewu_event_cloud_function
def wewu_api_delete_and_paste_inator(event: dict):
    parsed_body = delete_service_request_schema.load(event)
    job_repository.mark_jobs_as_cancelled([parsed_body["job_id"]])

    logger.info("Successfully marked job as cancelled", job_id=parsed_body["job_id"])
