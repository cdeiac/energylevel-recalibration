from datetime import datetime
from typing import List

from config.mongodb import MongoDB
from schemas.Respiration import Respiration


class RespirationRepository:
    # target DB
    mongoDb = MongoDB()
    __respirationDB = mongoDb.db['respiration']

    async def save(self, respiration: Respiration):
        # early return
        if not respiration:
            return {}

        return await self.__respirationDB.insert_one(respiration)

    async def save_many(self, respirationEntries: List[Respiration]):
        # early return
        if not respirationEntries:
            return {}

        return await self.__respirationDB.insert_many(respirationEntries)

    async def find_many(self, userId, timeStart: datetime, timeEnd: datetime):
        cursor = self.__respirationDB.find(
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
        cursor = self.__respirationDB.find({'userId': userId})
        return [doc async for doc in cursor]