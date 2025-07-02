from typing import List

from pydantic.schema import datetime, date

from config.mongodb import MongoDB
from schemas.bodyBattery import BodyBattery


class BodyBatteryRepository:
    """
    Repository for performing CRUD operations on the 'bodyBattery' collection in MongoDB.
    """

    # target DB
    mongoDb = MongoDB()
    __bodyBatteryDB = mongoDb.db['bodyBattery']

    async def save(self, bodyBattery: BodyBattery):
        """
        Saves a single BodyBattery document to the database.

        Parameters:
        -----------
        bodyBattery : BodyBattery
            The body battery data to insert.

        Returns:
        --------
        InsertOneResult or dict
            Result of the insert operation, or an empty dict if input is invalid.
        """
        if not bodyBattery:
            return {}

        return await self.__bodyBatteryDB.insert_one(bodyBattery)

    async def save_many(self, bodyBatteryEntries: List[BodyBattery]):
        """
        Saves multiple BodyBattery documents to the database.

        Parameters:
        -----------
        bodyBatteryEntries : List[BodyBattery]
            A list of body battery entries to insert.

        Returns:
        --------
        InsertManyResult or dict
            Result of the insert operation, or an empty dict if input is invalid.
        """
        if not bodyBatteryEntries:
            return {}

        return self.__bodyBatteryDB.insert_many(bodyBatteryEntries)

    async def find_many(self, userId, start: int, end: int):
        """
        Retrieves BodyBattery documents for a user within a time range.

        Parameters:
        -----------
        userId : str
            The user's unique identifier.
        start : int
            Start of the time range (inclusive) in epoch seconds.
        end : int
            End of the time range (inclusive) in epoch seconds.

        Returns:
        --------
        List[dict]
            A list of documents matching the criteria.
        """
        cursor = self.__bodyBatteryDB.find(
            {
                'userId': userId,
                'timestamp': {
                    '$gte': start,
                    '$lte': end
                }
            }
        )
        return [doc async for doc in cursor]

    async def find_all(self, userId: str):
        """
        Retrieves all BodyBattery documents for a user.

        Parameters:
        -----------
        userId : str
            The user's unique identifier.

        Returns:
        --------
        List[dict]
            All documents for the specified user.
        """
        cursor = self.__bodyBatteryDB.find({'userId': userId})
        return [doc async for doc in cursor]
