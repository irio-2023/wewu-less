import os

from pymongo import MongoClient

mongo_client = MongoClient(os.environ["MONGODB_URL"])
