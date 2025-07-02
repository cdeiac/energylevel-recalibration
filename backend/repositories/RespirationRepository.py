from datetime import datetime
from typing import List

from pydantic.schema import date

from config.mongodb import MongoDB
from schemas.Respiration import Respiration


class RespirationRepository:
    """
    Repository for managing Respiration data in the MongoDB 'respiration' collection.
    Provides methods to save and query respiration records for users.
    """

    # target DB
    mongoDb = MongoDB()
    __respirationDB = mongoDb.db['respiration']

    async def save(self, respiration: Respiration):
        """
        Saves a single respiration record to the database.

        Parameters:
        -----------
        respiration : Respiration
            A respiration document to insert.

        Returns:
        --------
        InsertOneResult or dict
            The result of the insert operation, or an empty dict if input is invalid.
        """
        if not respiration:
            return {}

        return await self.__respirationDB.insert_one(respiration)

    async def save_many(self, respirationEntries: List[Respiration]):
        """
        Saves multiple respiration records to the database.

        Parameters:
        -----------
        respirationEntries : List[Respiration]
            A list of respiration documents to insert.

        Returns:
        --------
        InsertManyResult or dict
            The result of the insert operation, or an empty dict if input is invalid.
        """
        if not respirationEntries:
            return {}

        return await self.__respirationDB.insert_many(respirationEntries)

    async def find_many(self, userId, dateStart: date, dateEnd: date):
        """
        Retrieves respiration records for a user within a date range.

        Parameters:
        -----------
        userId : str
            The user's unique identifier.
        dateStart : date
            Start date (inclusive).
        dateEnd : date
            End date (exclusive).

        Returns:
        --------
        List[dict]
            A list of respiration records matching the given range.
        """
        cursor = self.__respirationDB.find(
            {
                'userId': userId,
                'timestamp': {
                    '$gte': int(datetime.fromisoformat(dateStart.isoformat()).timestamp()),
                    '$lt': int(datetime.fromisoformat(dateEnd.isoformat()).timestamp())
                }
            }
        )
        return [doc async for doc in cursor]

    async def find_all(self, userId: str):
        """
        Retrieves all respiration records for a specific user.

        Parameters:
        -----------
        userId : str
            The user's unique identifier.

        Returns:
        --------
        List[dict]
            A list of all respiration records for the user.
        """
        cursor = self.__respirationDB.find({'userId': userId})
        return [doc async for doc in cursor]
