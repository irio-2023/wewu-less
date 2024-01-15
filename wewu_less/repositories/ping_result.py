from typing import Iterable, Tuple
from uuid import UUID

from pymongo import MongoClient
from pymongo.collection import Collection

from wewu_less.models.monitor_result import MonitorResult
from wewu_less.repositories.database import mongo_client as _mongo_client
from wewu_less.repositories.utils import sharding_step
from wewu_less.schemas.monitor_result import MonitorResultSchema

TIME_WINDOW_TO_MONITOR = 3000
monitor_result_schema = MonitorResultSchema()


def _parse_monitor_result(result: dict) -> MonitorResult:
    parsed_result = monitor_result_schema.load(result)
    return MonitorResult(**parsed_result)


class PingResultRepository:
    ping_results: Collection

    def __init__(self, mongo_client: MongoClient = _mongo_client):
        self.ping_results = mongo_client.job_database.monitor_result

    def get_pings_to_check(self, shard: int) -> Iterable[MonitorResult]:
        aggregation_query = [*sharding_step(shard)]

        results = list(
            map(_parse_monitor_result, self.ping_results.aggregate(aggregation_query))
        )

        def get_key(x: MonitorResult) -> Tuple[UUID, int]:
            return x.job_id, x.timestamp

        results.sort(key=get_key, reverse=True)
        return results
