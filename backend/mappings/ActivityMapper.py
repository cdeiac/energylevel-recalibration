from datetime import datetime

import pandas as pd
from pandas import DataFrame

from dtos.Activity import Activity as ActivityDTO
from enums.ActivityType import ActivityType
from schemas.Activity import Activity
from typing import List


class ActivityMapper:
    """
    A utility class for mapping ActivityDTO objects to Activity domain models.
    """

    @staticmethod
    def to_schema(activity: ActivityDTO) -> Activity:
        """
        Converts an ActivityDTO instance into an Activity domain model.

        This method calculates derived fields like `startTimeOffsetInSeconds`,
        `endTimeOffsetInSeconds`, and calendar attributes such as day of week and month
        based on the `startTimeInSeconds` timestamp.

        Parameters:
        -----------
        activity : ActivityDTO
            The data transfer object containing raw activity data.

        Returns:
        --------
        Activity
            A populated Activity model with enriched and structured data.
        """
        # Format timestamp and calculate offsets
        offset_start_time = activity.startTimeInSeconds
        offset_end_time = offset_start_time + activity.durationInSeconds
        date = datetime.fromtimestamp(offset_start_time).date()
        day_of_week = date.weekday()
        month = date.month

        return Activity(
            userId=activity.userId,
            userAccessToken=activity.userAccessToken,
            summaryId=activity.summaryId,
            activityId=activity.activityId,
            activityName=activity.activityName,
            activityDescription=activity.activityDescription,
            durationInSeconds=activity.durationInSeconds,
            startTimeOffsetInSeconds=offset_start_time,
            endTimeOffsetInSeconds=offset_end_time,
            activityType=ActivityType[activity.activityType],
            averageHeartRateInBeatsPerMinute=activity.averageHeartRateInBeatsPerMinute,
            averageRunCadenceInStepsPerMinute=activity.averageRunCadenceInStepsPerMinute,
            averageSpeedInMetersPerSecond=activity.averageSpeedInMetersPerSecond,
            averagePaceInMinutesPerKilometer=activity.averagePaceInMinutesPerKilometer,
            activeKilocalories=activity.activeKilocalories,
            distanceInMeters=activity.distanceInMeters,
            maxHeartRateInBeatsPerMinute=activity.maxHeartRateInBeatsPerMinute,
            maxPaceInMinutesPerKilometer=activity.maxPaceInMinutesPerKilometer,
            maxRunCadenceInStepsPerMinute=activity.maxRunCadenceInStepsPerMinute,
            maxSpeedInMetersPerSecond=activity.maxSpeedInMetersPerSecond,
            steps=activity.steps,
            totalElevationGainInMeters=activity.totalElevationGainInMeters,
            calendarDate=date,
            dayOfWeek=day_of_week,
            month=month
        )

    @staticmethod
    def to_dataframe(data: List[Activity]) -> DataFrame:
        """
        Converts a list of Activity objects into a pandas DataFrame.

        Parameters:
        -----------
        data : List[Activity]
            A list of Activity domain objects.

        Returns:
        --------
        DataFrame
            A pandas DataFrame containing structured activity data,
            with timestamps converted to datetime format and typed columns.
        """
        df = pd.DataFrame({
            'activityType': pd.Series(dtype='str'),
            'timeStart': pd.Series(dtype='int'),
            'timeEnd': pd.Series(dtype='int'),
            'steps': pd.Series(dtype='int'),
            'averageHeartRateInBeatsPerMinute': pd.Series(dtype='double'),
            'averageRunCadenceInStepsPerMinute': pd.Series(dtype='double'),
            'averageSpeedInMetersPerSecond': pd.Series(dtype='double'),
            'averagePaceInMinutesPerKilometer': pd.Series(dtype='double'),
            'activeKilocalories': pd.Series(dtype='double'),
            'maxHeartRateInBeatsPerMinute': pd.Series(dtype='double'),
            'distanceInMeters': pd.Series(dtype='double'),
            'maxPaceInMinutesPerKilometer': pd.Series(dtype='double'),
            'maxRunCadenceInStepsPerMinute': pd.Series(dtype='double'),
            'maxSpeedInMetersPerSecond': pd.Series(dtype='double'),
            'totalElevationGainInMeters': pd.Series(dtype='double'),
            'durationInSeconds': pd.Series(dtype='int'),
            'calendarDate': pd.Series(dtype='str'),
            'dayOfWeek': pd.Series(dtype='int'),
            'month': pd.Series(dtype='int')
        })

        df['activityType'] = [d.activityType.value for d in data]
        df['timeStart'] = [d.startTimeOffsetInSeconds for d in data]
        df['timeEnd'] = [d.endTimeOffsetInSeconds for d in data]
        df['steps'] = [d.steps for d in data]
        df['averageHeartRateInBeatsPerMinute'] = [d.averageHeartRateInBeatsPerMinute for d in data]
        df['averageRunCadenceInStepsPerMinute'] = [d.averageRunCadenceInStepsPerMinute for d in data]
        df['averageSpeedInMetersPerSecond'] = [d.averageSpeedInMetersPerSecond for d in data]
        df['averagePaceInMinutesPerKilometer'] = [d.averagePaceInMinutesPerKilometer for d in data]
        df['activeKilocalories'] = [d.activeKilocalories for d in data]
        df['maxHeartRateInBeatsPerMinute'] = [d.maxHeartRateInBeatsPerMinute for d in data]
        df['distanceInMeters'] = [d.distanceInMeters for d in data]
        df['maxPaceInMinutesPerKilometer'] = [d.maxPaceInMinutesPerKilometer for d in data]
        df['maxRunCadenceInStepsPerMinute'] = [d.maxRunCadenceInStepsPerMinute for d in data]
        df['maxSpeedInMetersPerSecond'] = [d.maxSpeedInMetersPerSecond for d in data]
        df['totalElevationGainInMeters'] = [d.totalElevationGainInMeters for d in data]
        df['durationInSeconds'] = [d.durationInSeconds for d in data]
        df['calendarDate'] = [d.calendarDate for d in data]
        df['dayOfWeek'] = [d.dayOfWeek for d in data]
        df['month'] = [d.month for d in data]

        df['timeStart'] = pd.to_datetime(df['timeStart'], unit='s')
        df['timeEnd'] = pd.to_datetime(df['timeEnd'], unit='s')
        return df
