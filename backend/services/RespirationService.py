import logging
from datetime import datetime
from typing import List

import pandas as pd

from mappings.RespirationMapper import RespirationMapper
from repositories.RespirationRepository import RespirationRepository
from schemas.Respiration import Respiration


class RespirationService:
    __log = logging.getLogger(__name__)
    __repository = RespirationRepository()

    async def save_many(self, respirationDetails):
        # early return
        if not respirationDetails.allDayRespiration: # respirationDetails
            return {}

        bodyBatteryEntries = []
        # map DTO to schema model
        for respiration in respirationDetails.allDayRespiration: # respirationDetails

            for key, value in respiration.timeOffsetEpochToBreaths.items():
                # map entry
                respirationEntry = RespirationMapper.from_respiration_detail(respiration, key, value).to_json()
                self.__log.debug(respirationEntry)
                bodyBatteryEntries.append(respirationEntry)
        # save
        await self.__repository.save_many(bodyBatteryEntries)
        return respirationDetails

    async def find_many(self, userId: str, timeStart: datetime, timeEnd: datetime):
        # parameter validation
        if not timeStart <= timeEnd:
            raise ValueError('timeStart must be before timeEnd!')

        # find entries
        result = await self.__repository.find_many(userId, timeStart, timeEnd)
        # map entries
        return [Respiration.parse_obj(res) for res in result]

    async def find_all(self, userId: str):
        # find entries
        result = await self.__repository.find_all(userId)
        # map entries
        return [Respiration.parse_obj(res) for res in result]

    async def find_all_to_dataframe(self, userId: str):
        # find entries
        result = await self.find_all(userId)
        # map to dataframe
        return self.__map_to_dataframe(result)


    def __map_to_dataframe(self, data: List[Respiration]):
        df = pd.DataFrame({
            'summaryId': pd.Series(dtype='str'),
            'timestamp': pd.Series(dtype='int'),
            'respiration': pd.Series(dtype='int'),
            'calendarDate': pd.Series(dtype='str'),
            'dayOfWeek': pd.Series(dtype='int'),
            'month': pd.Series(dtype='int')})

        df['summaryId'] = [d.summaryId for d in data]
        df['timestamp'] = [d.timestamp for d in data]
        df['respiration'] = [d.value for d in data]
        df['calendarDate'] = [d.calendarDate for d in data]
        df['dayOfWeek'] = [d.dayOfWeek for d in data]
        df['month'] = [d.month for d in data]

        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        return df

