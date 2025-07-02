from typing import List

from pydantic.schema import datetime

from config.mongodb import MongoDB
from schemas.Steps import Steps


class StepsRepository:
    """
    Repository for managing step data in the MongoDB 'steps' collection.
    Provides methods to save and retrieve step records for users.
    """

    # target DB
    mongoDb = MongoDB()
    __stepsDB = mongoDb.db['steps']

    async def save(self, steps: Steps):
        """
        Saves a single step record to the database.

        Parameters:
        -----------
        steps : Steps
            A step document to insert.

        Returns:
        --------
        InsertOneResult or dict
            The result of the insert operation, or an empty dict if input is invalid.
        """
        if not steps:
            return {}

        return await self.__stepsDB.insert_one(steps)

    async def save_many(self, steps: List[Steps]):
        """
        Saves multiple step records to the database.

        Parameters:
        -----------
        steps : List[Steps]
            A list of step documents to insert.

        Returns:
        --------
        InsertManyResult or dict
            The result of the insert operation, or an empty dict if input is invalid.
        """
        if not steps:
            return {}

        return self.__stepsDB.insert_many(steps)

    async def find(self, userAccessToken, timeStart: datetime, timeEnd: datetime):
        """
        Retrieves step records for a user within a specific time range.

        Parameters:
        -----------
        userAccessToken : str
            The access token identifying the user.
        timeStart : datetime
            Start of the time range (inclusive).
        timeEnd : datetime
            End of the time range (exclusive).

        Returns:
        --------
        List[dict]
            A list of step documents matching the query.
        """
        cursor = self.__stepsDB.find(
            {
                'userAccessToken': userAccessToken,
                'timestamp': {
                    '$gte': timeStart,
                    '$lt': timeEnd
                }
            }
        )
        return [doc async for doc in cursor]

    async def find_all(self, userId: str) -> List[Steps]:
        """
        Retrieves all step records for a specific user.

        Parameters:
        -----------
        userId : str
            The user's unique identifier.

        Returns:
        --------
        List[Steps]
            A list of all step documents for the user.
        """
        cursor = self.__stepsDB.find({'userId': userId})
        return [doc async for doc in cursor]
