import datetime
import logging
from typing import List

import pandas as pd

from mappings.ActivityMapper import ActivityMapper
from mappings.StepsMapper import StepsMapper
from repositories.ActivityRepository import ActivityRepository
from repositories.StepsRepository import StepsRepository
from schemas.Activity import Activity


class ActivityService:
    __log = logging.getLogger(__name__)
    __activity_repository = ActivityRepository()
    __steps_repository = StepsRepository()

    async def save_many(self, activities):
        # early return
        if not activities.activities:
            return {}

        activity_entries = []
        steps_entries = []
        # map DTO to schema model, save steps and activities separately
        for activity in activities.activities:
            # map activity
            activity_entry = ActivityMapper.from_activity(activity)
            activity_json = activity_entry.to_json()
            self.__log.debug(activity_json)
            activity_entries.append(activity_json)
            # resample data for steps
            steps_entries.extend(self.__resample_and_map_steps(activity_entry))

        # save
        await self.__activity_repository.save_many(activity_entries)
        await self.__steps_repository.save_many(steps_entries)
        return activity_entries

    async def find_many(self, userId: str, timeStart: datetime, timeEnd: datetime):
        # parameter validation
        if not timeStart <= timeEnd:
            raise ValueError('timeStart must be before timeEnd!')

        # find entries
        result = await self.__activity_repository.find(userId, timeStart, timeEnd)
        # map entries
        return [Activity.parse_obj(res) for res in result]

    async def find_all(self, userId: str):
        # find entries
        result = await self.__activity_repository.find_all(userId)
        # map entries
        return [Activity.parse_obj(res) for res in result]

    async def find_all_to_dataframe(self, userId: str):
        # find entries
        result = await self.find_all(userId)
        # map to dataframe
        return self.__map_to_dataframe(result)


    def __map_to_dataframe(self, data: List[Activity]):
        df = pd.DataFrame({
            'summaryId': pd.Series(dtype='str'),
            'activityType': pd.Series(dtype='str'),
            'timeStart': pd.Series(dtype='int'),
            'timeEnd': pd.Series(dtype='int'),
            'steps': pd.Series(dtype='int'),
            'calendarDate': pd.Series(dtype='str'),
            'dayOfWeek': pd.Series(dtype='int'),
            'month': pd.Series(dtype='int')})

        df['summaryId'] = [d.summaryId for d in data]
        df['activityType'] = [d.activityType for d in data]
        df['timeStart'] = [d.startTimeOffsetInSeconds for d in data]
        df['timeEnd'] = [d.endTimeOffsetInSeconds for d in data]
        df['steps'] = [d.steps for d in data]
        df['calendarDate'] = [d.calendarDate for d in data]
        df['dayOfWeek'] = [d.dayOfWeek for d in data]
        df['month'] = [d.month for d in data]

        df['timeStart'] = pd.to_datetime(df['timeStart'], unit='s')
        df['timeEnd'] = pd.to_datetime(df['timeEnd'], unit='s')
        return df


    @staticmethod
    def __resample_and_map_steps(activity: Activity):
        resampled_data = []
        current_timestamp = activity.startTimeOffsetInSeconds
        while current_timestamp <= activity.endTimeOffsetInSeconds:
            # add data in 3 minutes interval to match other data
            activity.timestamp = current_timestamp
            # map activity to steps
            resampled_data.append(StepsMapper.from_activity(activity).to_json())
            current_timestamp += 180
        # add resampled data
        return resampled_data

