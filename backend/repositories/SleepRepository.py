from datetime import datetime
from typing import List

from config.mongodb import MongoDB
from schemas.Sleep import Sleep


class SleepRepository:
    # target DB
    mongoDb = MongoDB()
    __sleepDB = mongoDb.db['sleep']

    async def save(self, sleep: Sleep):
        # early return
        if not sleep:
            return {}

        return await self.__sleepDB.insert_one(sleep)

    async def save_many(self, sleepEntries: List[Sleep]):
        # early return
        if not sleepEntries:
            return {}

        return self.__sleepDB.insert_many(sleepEntries)

    async def find_many(self, userId, timeStart: datetime, timeEnd: datetime):
        cursor = self.__sleepDB.find(
            {
                'userId': userId,
                'timestamp': {
                    '$gte': timeStart,
                    '$lt': timeEnd
                }
            }
        )
        return [doc async for doc in cursor]

    async def find_all(self, userId: str) -> List[Sleep]:
        cursor = self.__sleepDB.find({'userId': userId})
        return [doc async for doc in cursor]
