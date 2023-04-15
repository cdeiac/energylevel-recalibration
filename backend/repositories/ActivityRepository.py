
from typing import List

from pydantic.schema import datetime

from config.mongodb import MongoDB
from schemas.Activity import Activity


class ActivityRepository:
    # target DB
    mongoDb = MongoDB()
    __activitiesDB = mongoDb.db['activities']

    async def save(self, activity: Activity):
        # early return
        if not activity:
            return {}

        return await self.__activitiesDB.insert_one(activity)

    async def save_many(self, activities: List[Activity]):
        # early return
        if not activities:
            return {}

        return self.__activitiesDB.insert_many(activities)

    async def find(self, userAccessToken, timeStart: datetime, timeEnd: datetime):
        cursor = self.__activitiesDB.find(
            {
                'userAccessToken': userAccessToken,
                'timestamp': {
                    '$gte': timeStart,
                    '$lt': timeEnd
                }
            }
        )
        return [doc async for doc in cursor]

    async def find_all(self, userId: str) -> List[Activity]:
        cursor = self.__activitiesDB.find({'userId': userId})
        return [doc async for doc in cursor]

