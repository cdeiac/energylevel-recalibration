import logging
from datetime import datetime
from typing import List

import pandas as pd

from mappings import SleepMapper
from mappings.SleepMapper import SleepMapper
from dtos.sleep import Sleeps
from repositories.SleepRepository import SleepRepository
from repositories.SleepStatisticsRepository import SleepStatisticsRepository
from schemas.Sleep import Sleep
from schemas.SleepStatistics import SleepStatistics


class SleepService:
    __log = logging.getLogger(__name__)
    __repository = SleepRepository()
    __statsRepository = SleepStatisticsRepository()

    async def save_many(self, sleeps: Sleeps):
        # early return
        if not sleeps.sleeps:
            return {}

        mapped_entries = []
        mapped_stats_entries = []
        # map DTO to schema model
        for sleep in sleeps.sleeps:
            # map statistics only
            mapped_stats_entries.append(SleepMapper.to_sleep_stats(sleep).to_json())
            for sleepLevelTuple in sleep.sleepLevelsMap:
                if not sleepLevelTuple:
                    continue
                sleep_level_type = sleepLevelTuple[0]
                sleep_level_entries = sleepLevelTuple[1]
                # sleepLevelsMap might be empty
                if not sleep_level_entries:
                    continue
                for entry in sleep_level_entries:
                    # map entry
                    mapped_entry = SleepMapper.from_sleep(sleep, entry, sleep_level_type).to_json()
                    self.__log.debug(mapped_entry)
                    mapped_entries.append(mapped_entry)
        # save
        await self.__repository.save_many(mapped_entries)
        await self.__statsRepository.save_many(mapped_stats_entries)
        return mapped_entries

    async def find_many(self, userId: str, timeStart: datetime, timeEnd: datetime):
        # parameter validation
        if not timeStart <= timeEnd:
            raise ValueError('timeStart must be before timeEnd!')

        # find entries
        result = await self.__repository.find_many(userId, timeStart, timeEnd)
        # map entries
        return [Sleep.parse_obj(res) for res in result]

    async def find_all(self, userId: str):
        # find entries
        result = await self.__repository.find_all(userId)
        # map entries
        return [Sleep.parse_obj(res) for res in result]

    async def find_all_statistics(self, userId: str):
        # find entries
        result = await self.__statsRepository.find_all(userId)
        # map entries
        return [SleepStatistics.parse_obj(res) for res in result]

    async def find_all_to_dataframe(self, userId: str):
        # find entries
        result = await self.find_all(userId)
        # map to dataframe
        return self.__map_to_dataframe(result)


    def __map_to_dataframe(self, data: List[Sleep]):
        df = pd.DataFrame({
            'summaryId': pd.Series(dtype='str'),
            'timeStart': pd.Series(dtype='int'),
            'timeEnd': pd.Series(dtype='int'),
            'sleepLevelType': pd.Series(dtype='str'),
            'calendarDate': pd.Series(dtype='str'),
            'dayOfWeek': pd.Series(dtype='int'),
            'month': pd.Series(dtype='int')})

        df['summaryId'] = [d.summaryId for d in data]
        df['timeStart'] = [d.startTimeOffsetInSeconds for d in data]
        df['timeEnd'] = [d.endTimeOffsetInSeconds for d in data]
        df['sleepLevelType'] = [d.sleepLevelType for d in data]
        df['calendarDate'] = [d.calendarDate for d in data]
        df['dayOfWeek'] = [d.dayOfWeek for d in data]
        df['month'] = [d.month for d in data]

        df['timeStart'] = pd.to_datetime(df['timeStart'], unit='s')
        df['timeEnd'] = pd.to_datetime(df['timeEnd'], unit='s')
        return df
