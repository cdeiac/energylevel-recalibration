import logging
from datetime import datetime
from typing import List

import pandas as pd

from mappings.StressMapper import StressLevelMapper
from repositories.StressLevelRepository import StressLevelRepository
from schemas.stress import StressLevel


class StressLevelService:
    __log = logging.getLogger(__name__)
    __repository = StressLevelRepository()

    async def save_many(self, stressDetails):
        # early return
        if not stressDetails.stressDetails:
            return {}

        stressEntries = []
        # map DTO to schema model
        for stressDetail in stressDetails.stressDetails:

            for key, value in stressDetail.timeOffsetStressLevelValues.items():
                # map entry
                stressEntry = StressLevelMapper.from_stress_detail(stressDetail, key, value).to_json()
                self.__log.debug(stressEntry)
                stressEntries.append(stressEntry)
        # save
        await self.__repository.save_many(stressEntries)
        return stressDetails

    async def find_many(self, userId: str, timeStart: datetime, timeEnd: datetime):
        # parameter validation
        if not timeStart <= timeEnd:
            raise ValueError('timeStart must be before timeEnd!')

        # find entries
        result = await self.__repository.find_many(userId, timeStart, timeEnd)
        # map entries
        return [StressLevel.parse_obj(res) for res in result]

    async def find_all(self, userId: str):
        # find entries
        result = await self.__repository.find_all(userId)
        # map entries
        return [StressLevel.parse_obj(res) for res in result]

    async def find_all_to_dataframe(self, userId: str):
        # find entries
        result = await self.find_all(userId)
        # map to dataframe
        return self.__map_to_dataframe(result)

    def __map_to_dataframe(self, data: List[StressLevel]):
        df = pd.DataFrame({
            'summaryId': pd.Series(dtype='str'),
            'timestamp': pd.Series(dtype='int'),
            'stressLevel': pd.Series(dtype='int'),
            'calendarDate': pd.Series(dtype='str'),
            'dayOfWeek': pd.Series(dtype='int'),
            'month': pd.Series(dtype='int')})

        df['summaryId'] = [d.summaryId for d in data]
        df['stressLevel'] = [d.value for d in data]
        df['timestamp'] = [d.timestamp for d in data]
        df['calendarDate'] = [d.calendarDate for d in data]
        df['dayOfWeek'] = [d.dayOfWeek for d in data]
        df['month'] = [d.month for d in data]

        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        return df

