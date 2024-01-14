from typing import List


def sharding_step(shard: int) -> List[dict]:
    return [
        {"$filter": {}},
        {
            "$addFields": {"shard": shard},
        },
        {"$match": {"shard": shard}},
    ]
