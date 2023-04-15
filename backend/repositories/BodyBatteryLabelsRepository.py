from typing import List
from pydantic.schema import datetime
from pymongo import ReturnDocument

from config.mongodb import MongoDB
from schemas.BodyBatteryLabel import BodyBatteryLabel


class BodyBatteryLabelsRepository:
    # target DB
    mongoDb = MongoDB()
    __bodyBatteryLabelsDB = mongoDb.db['bodyBattery']

    async def save(self, bodyBatteryLabel: BodyBatteryLabel):
        # early return
        if not bodyBatteryLabel:
            return {}

        return await self.__bodyBatteryLabelsDB.insert_one(bodyBatteryLabel)

    async def save_many(self, userId: str, bodyBatteryLabels: List[BodyBatteryLabel]):
        # early return
        if not bodyBatteryLabels:
            return {}
        # TODO: Upsert
        return self.__bodyBatteryLabelsDB.insert_many(userId, bodyBatteryLabels)

    async def update_many(self, userId: str, labels: List[BodyBatteryLabel]):
        # early return
        if not labels:
            return {}

        for label in labels:
            self.__bodyBatteryLabelsDB.update_one(
                { 'userId': userId, 'timestamp':  int(label.timestamp) },
                { '$set': { 'label' : int(label.label)} }
            )

    async def find_many(self, userId, timeStart: datetime, timeEnd: datetime):
        cursor = self.__bodyBatteryLabelsDB.find(
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
        cursor = self.__bodyBatteryLabelsDB.find({'userId': userId})
        return [doc async for doc in cursor]

