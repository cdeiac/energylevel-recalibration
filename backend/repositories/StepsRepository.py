
from typing import List

from pydantic.schema import datetime

from config.mongodb import MongoDB
from schemas.Steps import Steps


class StepsRepository:
    # target DB
    mongoDb = MongoDB()
    __stepsDB = mongoDb.db['steps']

    async def save(self, steps: Steps):
        # early return
        if not steps:
            return {}

        return await self.__stepsDB.insert_one(steps)

    async def save_many(self, steps: List[Steps]):
        # early return
        if not steps:
            return {}

        return self.__stepsDB.insert_many(steps)

    async def find(self, userAccessToken, timeStart: datetime, timeEnd: datetime):
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
        cursor = self.__stepsDB.find({'userId': userId})
        return [doc async for doc in cursor]

