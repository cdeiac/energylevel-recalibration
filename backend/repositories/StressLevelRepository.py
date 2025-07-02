from datetime import datetime
from typing import List

from pydantic.schema import date

from config.mongodb import MongoDB
from schemas.stress import StressLevel


class StressLevelRepository:
    """
    Repository for managing StressLevel data in the MongoDB 'stressLevel' collection.
    Provides methods to save and retrieve stress records for users.
    """

    # target DB
    mongoDb = MongoDB()
    __stressLevelDB = mongoDb.db['stressLevel']

    async def save(self, stressLevel: StressLevel):
        """
        Saves a single stress level record to the database.

        Parameters:
        -----------
        stressLevel : StressLevel
            A stress level document to insert.

        Returns:
        --------
        InsertOneResult or dict
            The result of the insert operation, or an empty dict if input is invalid.
        """
        if not stressLevel:
            return {}

        return await self.__stressLevelDB.insert_one(stressLevel)

    async def save_many(self, stressEntries: List[StressLevel]):
        """
        Saves multiple stress level records to the database.

        Parameters:
        -----------
        stressEntries : List[StressLevel]
            A list of stress level documents to insert.

        Returns:
        --------
        InsertManyResult or dict
            The result of the insert operation, or an empty dict if input is invalid.
        """
        if not stressEntries:
            return {}

        return self.__stressLevelDB.insert_many(stressEntries)

    async def find_many(self, userId, start: int, end: int):
        """
        Retrieves stress level records for a user within a specific time range.

        Parameters:
        -----------
        userId : str
            The user's unique identifier.
        start : int
            Start of the time range (inclusive), in epoch seconds.
        end : int
            End of the time range (inclusive), in epoch seconds.

        Returns:
        --------
        List[dict]
            A list of stress level documents that match the criteria.
        """
        cursor = self.__stressLevelDB.find(
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
        Retrieves all stress level records for a specific user.

        Parameters:
        -----------
        userId : str
            The user's unique identifier.

        Returns:
        --------
        List[dict]
            A list of all stress level documents for the user.
        """
        cursor = self.__stressLevelDB.find({'userId': userId})
        return [doc async for doc in cursor]
