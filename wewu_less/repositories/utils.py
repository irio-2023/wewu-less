from typing import List


def sharding_step(shard: int) -> List[dict]:
    return [
        {
            "$addFields": {"shard": shard},
        },
        {"$match": {"shard": shard}},
    ]
