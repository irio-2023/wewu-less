import base64
import json
import random
from uuid import UUID

from wewu_less.models.geo_region import GeoRegion

r = random.Random("wewu-integration")


def create_event_mock(payload: dict) -> dict:
    return {"data": base64.b64encode(json.dumps(payload).encode())}


def create_job_request(job_id: UUID) -> dict:
    return {
        "jobId": str(job_id),
        "serviceUrl": "https://xyz.com",
        "geoRegions": [GeoRegion.US_EAST.value],
        "primaryAdmin": {"email": "xyz@abc.pl"},
        "secondaryAdmin": {"phoneNumber": "123456789"},
        "pollFrequencySecs": 5,
        "alertingWindowNumberOfCalls": r.randint(10, 20),
        "alertingWindowCallsFailCount": r.randint(5, 9),
        "ackTimeout": r.randint(5, 30),
    }
