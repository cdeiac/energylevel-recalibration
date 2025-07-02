import logging
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
            activity_entry = ActivityMapper.to_schema(activity)
            activity_json = activity_entry.to_json()
            self.__log.debug(activity_json)
            activity_entries.append(activity_json)
            # resample data for steps
            steps_entries.extend(self.__resample_and_map_steps(activity_entry))

        # save
        await self.__activity_repository.save_many(activity_entries)
        await self.__steps_repository.save_many(steps_entries)
        return activity_entries

    async def find_many(self, userId: str, start: int, end: int):
        # parameter validation
        if not start <= end:
            raise ValueError('start must be before end!')

        # find entries
        result = await self.__activity_repository.find(userId, start, end)
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
        return ActivityMapper.to_dataframe(data=result)


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

