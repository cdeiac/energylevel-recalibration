from datetime import datetime
from typing import List

from config.mongodb import MongoDB
from schemas.Sleep import Sleep
from schemas.SleepStatistics import SleepStatistics


class SleepStatisticsRepository:
    """
    Repository for managing sleep statistics in the MongoDB 'sleepStatistics' collection.
    Provides methods to save and retrieve summarized sleep data for users.
    """

    # target DB
    mongoDb = MongoDB()
    __sleepStatsDB = mongoDb.db['sleepStatistics']

    async def save_many(self, sleepEntries: List[SleepStatistics]):
        """
        Saves multiple sleep statistics entries to the database.

        Parameters:
        -----------
        sleepEntries : List[SleepStatistics]
            A list of sleep statistics documents to insert.

        Returns:
        --------
        InsertManyResult or dict
            The result of the insert operation, or an empty dict if input is invalid.
        """
        if not sleepEntries:
            return {}

        return self.__sleepStatsDB.insert_many(sleepEntries)

    async def find_many(self, userId, start: int, end: int):
        """
        Retrieves sleep statistics for a user within a given time range.

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
            A list of sleep statistics documents matching the criteria.
        """
        cursor = self.__sleepStatsDB.find(
            {
                'userId': userId,
                'timestamp': {
                    '$gte': start,
                    '$lte': end
                }
            }
        )
        return [doc async for doc in cursor]

    async def find_one(self, userId, time: datetime):
        """
        Retrieves a single sleep statistics record for a user on a specific date.

        Parameters:
        -----------
        userId : str
            The user's unique identifier.
        time : datetime
            The datetime object used to match `calendarDate`.

        Returns:
        --------
        List[dict]
            A list of documents matching the given user and calendar date.
        """
        cursor = self.__sleepStatsDB.find(
            {
                'userId': userId,
                'calendarDate': {
                    '$eq': time.date().isoformat()
                }
            }
        )
        return [doc async for doc in cursor]

    async def find_all(self, userId: str) -> List[Sleep]:
        """
        Retrieves all sleep statistics records for a specific user.

        Parameters:
        -----------
        userId : str
            The user's unique identifier.

        Returns:
        --------
        List[Sleep]
            All sleep statistics documents for the specified user.
        """
        cursor = self.__sleepStatsDB.find({'userId': userId})
        return [doc async for doc in cursor]
