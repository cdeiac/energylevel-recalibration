from datetime import datetime
from typing import List

from config.mongodb import MongoDB
from schemas.Sleep import Sleep
from schemas.SleepStatistics import SleepStatistics


class SleepStatisticsRepository:
    # target DB
    mongoDb = MongoDB()
    __sleepStatsDB = mongoDb.db['sleepStatistics']

    async def save_many(self, sleepEntries: List[SleepStatistics]):
        # early return
        if not sleepEntries:
            return {}

        return self.__sleepStatsDB.insert_many(sleepEntries)

    async def find_many(self, userId, timeStart: datetime, timeEnd: datetime):
        cursor = self.__sleepStatsDB.find(
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
        cursor = self.__sleepStatsDB.find({'userId': userId})
        return [doc async for doc in cursor]
