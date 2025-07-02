from typing import List

from pydantic.schema import datetime, date

from config.mongodb import MongoDB
from schemas.Activity import Activity


class ActivityRepository:
    """
    Repository for interacting with the 'activities' collection in MongoDB.
    Provides methods to save and retrieve Activity documents.
    """

    # target DB
    mongoDb = MongoDB()
    __activitiesDB = mongoDb.db['activities']

    async def save(self, activity: Activity):
        """
        Saves a single activity document to the database.

        Parameters:
        -----------
        activity : Activity
            The activity object to be inserted.

        Returns:
        --------
        InsertOneResult or dict
            The result of the insert operation, or an empty dict if the input is invalid.
        """
        # early return
        if not activity:
            return {}

        return await self.__activitiesDB.insert_one(activity)

    async def save_many(self, activities: List[Activity]):
        """
        Saves multiple activity documents to the database.

        Parameters:
        -----------
        activities : List[Activity]
            A list of activity objects to be inserted.

        Returns:
        --------
        InsertManyResult or dict
            The result of the insert_many operation, or an empty dict if the input is invalid.
        """
        # early return
        if not activities:
            return {}

        return self.__activitiesDB.insert_many(activities)

    async def find(self, userId: str, start: int, end: int):
        """
        Finds activity documents for a user within a specified time range.

        Parameters:
        -----------
        userId : str
            The ID of the user.
        start : int
            Start of the time range (epoch seconds).
        end : int
            End of the time range (epoch seconds).

        Returns:
        --------
        List[dict]
            A list of activity documents that match the criteria.
        """
        cursor = self.__activitiesDB.find(
            {
                'userId': userId,
                'startTimeOffsetInSeconds': {
                    '$gte': start,
                    '$lte': end
                }
            }
        )
        return [doc async for doc in cursor]

    async def find_all(self, userId: str) -> List[Activity]:
        """
        Finds all activity documents for a given user.

        Parameters:
        -----------
        userId : str
            The ID of the user.

        Returns:
        --------
        List[Activity]
            A list of all activity documents for the specified user.
        """
        cursor = self.__activitiesDB.find({'userId': userId})
        return [doc async for doc in cursor]
