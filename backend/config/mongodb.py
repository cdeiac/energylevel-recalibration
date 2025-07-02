import datetime
import pymongo
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import OperationFailure
from starlette.config import Config
from schemas.bodyBattery import BodyBattery


class MongoDB:
    """
    A class to manage the connection to a MongoDB instance and initialize collections.

    Attributes:
    -----------
    client : AsyncIOMotorClient
        The MongoDB client connection.
    db : Database
        The active MongoDB database.
    """

    client = None
    db = None

    def __init__(self):
        """
        Initializes the MongoDB object and establishes a connection to the database.
        """
        self.__establish_db_connection()

    def init_mongodb(self):
        """
        Re-establishes the MongoDB connection.
        Useful for resetting or reconnecting at runtime.
        """
        self.__establish_db_connection()

    def stop_mongodb(self):
        """
        Closes the connection to the MongoDB instance.
        """
        self.client.close()

    def __establish_db_connection(self):
        """
        Establishes a connection to the MongoDB instance using configuration
        from an environment file and initializes the database client and reference.
        """
        config = Config('.env')
        self.client = AsyncIOMotorClient(config.get('MONGO_URI'))
        # For synchronous client use:
        # self.client = pymongo.MongoClient(config.get('MONGO_URI'))
        self.db = self.client[config.get('MONGO_INITDB_DATABASE')]

    def __init_collections(self):
        """
        Initializes required collections in the database.
        Currently sets up 'bodyBattery' and 'stressLevel' as time-series collections.
        """
        self.__init_collection("bodyBattery")
        self.__init_collection("stressLevel")

    def __init_collection(self, name):
        """
        Initializes a single time-series collection in the database.
        If the collection already exists, it validates it.
        If not, it creates the collection with time-series configuration.

        Parameters:
        -----------
        name : str
            The name of the collection to initialize.
        """
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
