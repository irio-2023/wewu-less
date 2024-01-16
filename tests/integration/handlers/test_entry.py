import uuid

from pymongo.collection import Collection

from tests.integration.mongo import job_fixture
from tests.integration.utils import create_event_mock, create_job_request
from wewu_less.handlers.entry import (
    wewu_api_copy_and_paste_inator,
    wewu_api_delete_and_paste_inator,
)
from wewu_less.models.geo_region import GeoRegion


def test_copy_inator_should_insert_job(jobs_collection: Collection):
    job_id = uuid.uuid4()

    job_request = create_job_request(job_id)

    db_jobs = list(jobs_collection.find({}))
    assert len(db_jobs) == 0

    wewu_api_copy_and_paste_inator(create_event_mock(job_request))

    db_jobs = list(jobs_collection.find({}))

    assert len(db_jobs) == 1
    assert db_jobs[0]["jobId"] == str(job_id)


def test_delete_inator_should_mark_job_as_cancelled(jobs_collection: Collection):
    job1_id = uuid.uuid4()
    job2_id = uuid.uuid4()

    job_fixture(job1_id, jobs_collection)
    job_fixture(job2_id, jobs_collection)

    db_jobs = list(jobs_collection.find({}))
    assert len(db_jobs) == 2
    assert not any(map(lambda x: bool(x["isCancelled"]), db_jobs))

    wewu_api_delete_and_paste_inator(
        create_event_mock(
            {"jobId": str(job1_id), "geoRegions": [GeoRegion.US_EAST.value]}
        )
    )

    job1 = jobs_collection.find_one({"jobId": str(job1_id)})
    job2 = jobs_collection.find_one({"jobId": str(job2_id)})

    assert job1["isCancelled"]
    assert not job2["isCancelled"]
