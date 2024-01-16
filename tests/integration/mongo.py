from typing import Optional
from uuid import UUID

import pytest
from pymongo.collection import Collection

from tests.integration.utils import create_job_request
from wewu_less.models.job import JobModel
from wewu_less.repositories.database import mongo_client
from wewu_less.schemas.job import JobSchema
from wewu_less.schemas.register_request import RegisterServiceRequestSchema

job_schema = JobSchema()
register_service_schema = RegisterServiceRequestSchema()


@pytest.fixture
def jobs_collection():
    jobs_collection: Collection = mongo_client.job_database.jobs
    yield jobs_collection
    jobs_collection.drop()


def job_fixture(job_id: UUID, jobs_collection: Optional[Collection] = None) -> JobModel:
    job_request = create_job_request(job_id)
    model = JobModel.from_register_service_request(
        register_service_schema.load(job_request)
    )

    job_dict = job_schema.dump(model)

    if jobs_collection is not None:
        jobs_collection.insert_one(job_dict)

    return model
