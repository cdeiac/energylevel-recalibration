import datetime

import pymongo
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import OperationFailure
from starlette.config import Config

from schemas.bodyBattery import BodyBattery


class MongoDB:
    client = None
    db = None

    def __init__(self):
        self.__establish_db_connection()

    def init_mongodb(self):
        self.__establish_db_connection()


    def stop_mongodb(self):
        self.client.close()

    # establish connection to MongoDB instance
    def __establish_db_connection(self):
        # load config
        config = Config('.env')
        # init MongoDB client & database
        self.client = AsyncIOMotorClient(config.get('MONGO_URI'))
        #self.client = pymongo.MongoClient(config.get('MONGO_URI'))
        self.db = self.client[config.get('MONGO_INITDB_DATABASE')]

    # initiate collections
    def __init_collections(self):
        self.__init_collection("bodyBattery")
        self.__init_collection("stressLevel")

    # initiate a single collection
    def __init_collection(self, name):
        try:
            self.db.validate_collection(name)
        except OperationFailure:
            self.db.create_collection(
                name,
                timeseries={
                    "timeField": "timestamp",
                    "metaField": "dataType",
                    "granularity": "seconds"
                }
            )
