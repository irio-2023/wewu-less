import flask
from pymongo.collection import Collection

from wewu_less.logging import get_logger
from wewu_less.repositories.database import mongo_client

tester_client_collection: Collection = mongo_client.test.tester_client
logger = get_logger()


# This is raw cloud function for testing purposes, it doesn't follow clean code guidelines
def wewu_tester(request: flask.Request):
    if request.method == "GET":
        try:
            document = tester_client_collection.find_one()
            status = document["status_code"]
            return status
        except Exception:
            logger.exception(
                "Failed to retrieve tester record from database, returning 200"
            )
            return 200
    elif request.method == "POST":
        body = request.get_json()
        new_status_code = body["status_code"]
        tester_client_collection.update_many(
            {}, {"status_code": int(new_status_code)}, upsert=True
        )
        return 200
