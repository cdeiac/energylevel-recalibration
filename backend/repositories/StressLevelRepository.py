from datetime import datetime
from typing import List

from config.mongodb import MongoDB
from schemas.stress import StressLevel


class StressLevelRepository:
    # target DB
    mongoDb = MongoDB()
    __stressLevelDB = mongoDb.db['stressLevel']

    async def save(self, stressLevel: StressLevel):
        # early return
        if not stressLevel:
            return {}

        return await self.__stressLevelDB.insert_one(stressLevel)

    async def save_many(self, stressEntries: List[StressLevel]):
        # early return
        if not stressEntries:
            return {}

        return self.__stressLevelDB.insert_many(stressEntries)

    async def find_many(self, userId, timeStart: datetime, timeEnd: datetime):
        cursor = self.__stressLevelDB.find(
            {
                'userId': userId,
                'timestamp': {
                    '$gte': timeStart,
                    '$lt': timeEnd
                }
            }
        )
        return [doc async for doc in cursor]

    async def find_all(self, userId: str):

        cursor = self.__stressLevelDB.find({'userId': userId})
        return [doc async for doc in cursor]