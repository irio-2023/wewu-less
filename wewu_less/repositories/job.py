import dataclasses
from datetime import datetime, timezone
from typing import Iterable
from uuid import UUID

from pymongo import MongoClient
from pymongo.collection import Collection

from wewu_less.models.job import JobModel
from wewu_less.repositories.database import mongo_client as _mongo_client
from wewu_less.schemas.job import JobSchema

job_schema = JobSchema()


class JobRepository:
    jobs: Collection

    def __init__(self, mongo_client: MongoClient = _mongo_client):
        self.jobs = mongo_client.job_database.jobs

    @staticmethod
    def _mongo_to_model(mongo_job: dict) -> JobModel:
        parsed_job = job_schema.load(mongo_job)
        return JobModel(**parsed_job)

    @staticmethod
    def _model_to_mongo(model: JobModel) -> dict:
        return job_schema.dump(model)

    @staticmethod
    def _get_current_time() -> int:
        return int(datetime.now(timezone.utc).timestamp())

    def get_expired_jobs(self) -> list[JobModel]:
        mongo_query = {
            "expirationTimestamp": {"$lte": self._get_current_time()},
            "isCancelled": False,
        }

        mongo_job_iterable = self.jobs.find(mongo_query)

        return list(map(self._mongo_to_model, mongo_job_iterable))

    def save_new_job(self, job: JobModel):
        job_dict = dataclasses.asdict(job)
        self.jobs.insert_one(job_schema.dump(job_dict))

    def update_expiration_date(
        self, job_ids: Iterable[UUID], expiration_threshold: int
    ):
        job_ids = [str(job_id) for job_id in job_ids]
        query = {"jobId": {"$in": job_ids}}

        new_values = {
            "$set": {
                "expirationTimestamp": self._get_current_time() + expiration_threshold
            }
        }
        self.jobs.update_many(query, new_values)
