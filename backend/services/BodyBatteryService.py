import datetime
import logging
from typing import List

import pandas as pd

from mappings.BodyBatteryMapper import BodyBatteryMapper
from repositories.BodyBatteryLabelsRepository import BodyBatteryLabelsRepository
from repositories.BodyBatteryRepository import BodyBatteryRepository
from dtos.BodyBatteryLabel import BodyBatteryLabel
from schemas.bodyBattery import BodyBattery


class BodyBatteryService:
    __log = logging.getLogger(__name__)
    __repository = BodyBatteryRepository()
    __label_repository = BodyBatteryLabelsRepository()

    async def save_many(self, stressDetails):
        # early return
        if not stressDetails.stressDetails:
            return {}

        bodyBatteryEntries = []
        # map DTO to schema model
        for stressDetail in stressDetails.stressDetails:

            for key, value in stressDetail.timeOffsetBodyBatteryValues.items():
                # map entry
                bodyBatteryEntry = BodyBatteryMapper.from_stress_detail(stressDetail, key, value).to_json()
                self.__log.debug(bodyBatteryEntry)
                bodyBatteryEntries.append(bodyBatteryEntry)
        # save
        await self.__repository.save_many(bodyBatteryEntries)
        return stressDetails

    async def find_many(self, userAccessToken: str, timeStart: datetime, timeEnd: datetime):
        # parameter validation
        if not timeStart <= timeEnd:
            raise ValueError('timeStart must be before timeEnd!')

        # find entries
        result = await self.__repository.find_many(userAccessToken, timeStart, timeEnd)
        # map entries
        return [BodyBattery.parse_obj(res) for res in result]

    async def find_all(self, userId: str):
        # find entries
        result = await self.__repository.find_all(userId)
        # map entries
        entries = [BodyBattery.parse_obj(res) for res in result]
        # if there is a label, we set it as value for the returned entries
        for entry in entries:
            if entry.label is not None:
                entry.value = entry.label
        return entries

    async def find_all_to_dataframe(self, userId: str):
        # find entries
        result = await self.find_all(userId)
        # map to dataframe
        return self.__map_to_dataframe(result)

    async def label_body_battery(self, userId: str, labels: List[BodyBatteryLabel]):
        return await self.__label_repository.update_many(userId, labels)


    def __map_to_dataframe(self, data: List[BodyBattery]):
        df = pd.DataFrame({
            'summaryId': pd.Series(dtype='str'),
            'timestamp': pd.Series(dtype='int'),
            'bodyBattery': pd.Series(dtype='int'),
            'calendarDate': pd.Series(dtype='str'),
            'dayOfWeek': pd.Series(dtype='int'),
            'month': pd.Series(dtype='int')})

        df['summaryId'] = [d.summaryId for d in data]
        df['bodyBattery'] = [d.value for d in data]
        df['timestamp'] = [d.timestamp for d in data]
        df['calendarDate'] = [d.calendarDate for d in data]
        df['dayOfWeek'] = [d.dayOfWeek for d in data]
        df['month'] = [d.month for d in data]

        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        return df

