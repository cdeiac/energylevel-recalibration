
from typing import List

from pydantic.schema import datetime

from config.mongodb import MongoDB
from schemas.bodyBattery import BodyBattery


class BodyBatteryRepository:
    # target DB
    mongoDb = MongoDB()
    __bodyBatteryDB = mongoDb.db['bodyBattery']

    async def save(self, bodyBattery: BodyBattery):
        # early return
        if not bodyBattery:
            return {}

        return await self.__bodyBatteryDB.insert_one(bodyBattery)

    async def save_many(self, bodyBatteryEntries: List[BodyBattery]):
        # early return
        if not bodyBatteryEntries:
            return {}

        return self.__bodyBatteryDB.insert_many(bodyBatteryEntries)

    async def find_many(self, userId, timeStart: datetime, timeEnd: datetime):
        cursor = self.__bodyBatteryDB.find(
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
        cursor = self.__bodyBatteryDB.find({'userId': userId})
        return [doc async for doc in cursor]

