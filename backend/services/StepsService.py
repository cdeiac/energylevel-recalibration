import datetime
import logging
from typing import List

import pandas as pd

from repositories.StepsRepository import StepsRepository
from schemas.Steps import Steps


class StepsService:
    __log = logging.getLogger(__name__)
    __steps_repository = StepsRepository()

    async def find_many(self, userId: str, timeStart: datetime, timeEnd: datetime):
        # parameter validation
        if not timeStart <= timeEnd:
            raise ValueError('timeStart must be before timeEnd!')

        # find entries
        result = await self.__steps_repository.find(userId, timeStart, timeEnd)
        # map entries
        return [Steps.parse_obj(res) for res in result]

    async def find_all(self, userId: str):
        # find entries
        result = await self.__steps_repository.find_all(userId)
        # map entries
        return [Steps.parse_obj(res) for res in result]

    async def find_all_to_dataframe(self, userId: str):
        # find entries
        result = await self.find_all(userId)
        # map to dataframe
        return self.__map_to_dataframe(result)


    def __map_to_dataframe(self, data: List[Steps]):
        df = pd.DataFrame({
            'summaryId': pd.Series(dtype='str'),
            'timestamp': pd.Series(dtype='int'),
            'steps': pd.Series(dtype='int'),
            'calendarDate': pd.Series(dtype='str'),
            'dayOfWeek': pd.Series(dtype='int'),
            'month': pd.Series(dtype='int')})

        df['summaryId'] = [d.summaryId for d in data]
        df['timestamp'] = [d.timestamp for d in data]
        df['value'] = [d.value for d in data]

        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        return df

