from datetime import datetime
from typing import List

from pydantic.schema import date

from config.mongodb import MongoDB
from schemas.Sleep import Sleep


class SleepRepository:
    """
    Repository for managing Sleep data in the MongoDB 'sleep' collection.
    Provides methods to save and retrieve sleep records for users.
    """

    # target DB
    mongoDb = MongoDB()
    __sleepDB = mongoDb.db['sleep']

    async def save(self, sleep: Sleep):
        """
        Saves a single sleep record to the database.

        Parameters:
        -----------
        sleep : Sleep
            A sleep document to be inserted.

        Returns:
        --------
        InsertOneResult or dict
            The result of the insert operation, or an empty dict if input is invalid.
        """
        if not sleep:
            return {}

        return await self.__sleepDB.insert_one(sleep)

    async def save_many(self, sleepEntries: List[Sleep]):
        """
        Saves multiple sleep records to the database.

        Parameters:
        -----------
        sleepEntries : List[Sleep]
            A list of sleep documents to insert.

        Returns:
        --------
        InsertManyResult or dict
            The result of the insert operation, or an empty dict if input is invalid.
        """
        if not sleepEntries:
            return {}

        return self.__sleepDB.insert_many(sleepEntries)

    async def find_many(self, userId, start: int, end: int):
        """
        Retrieves sleep records for a user within a time range.

        Parameters:
        -----------
        userId : str
            The user's unique identifier.
        start : int
            Start of the time range (inclusive), as epoch seconds.
        end : int
            End of the time range (inclusive), as epoch seconds.

        Returns:
        --------
        List[dict]
            A list of sleep records matching the specified criteria.
        """
        cursor = self.__sleepDB.find(
            {
                'userId': userId,
                'timestamp': {
                    '$gte': start,
                    '$lte': end
                }
            }
        )
        return [doc async for doc in cursor]

    async def find_all(self, userId: str) -> List[Sleep]:
        """
        Retrieves all sleep records for a specific user.

        Parameters:
        -----------
        userId : str
            The user's unique identifier.

        Returns:
        --------
        List[Sleep]
            A list of all sleep documents for the user.
        """
        cursor = self.__sleepDB.find({'userId': userId})
        return [doc async for doc in cursor]
