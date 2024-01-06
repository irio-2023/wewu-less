from datetime import datetime, timezone

from bson import ObjectId

from pymongo import MongoClient
from pymongo.collection import Collection

from wewu_less.models.job import JobModel
from wewu_less.schemas.job import JobSchema

job_schema = JobSchema()


class JobRepository:
    jobs: Collection

    def __init__(self, client: MongoClient):
        self.jobs = client.job_database.jobs

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

        mongo_job_iterable = list(self.jobs.find(mongo_query))
        for mongo_job in mongo_job_iterable:
            object_id: ObjectId = mongo_job["_id"]
            mongo_job["_id"] = str(object_id)

        return list(map(self._mongo_to_model, mongo_job_iterable))

    def update_expiration_date(self, job_ids: list[str], expiration_threshold: int):
        query = {"_id": {"$in": job_ids}}

        new_values = {
            "expirationTimestamp": self._get_current_time() + expiration_threshold
        }
        self.jobs.update_many(query, new_values)
