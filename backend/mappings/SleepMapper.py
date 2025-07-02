from datetime import datetime
from typing import List

import pandas as pd
from pandas import DataFrame

from dtos.sleep import Sleep as SleepModel, SleepLevel
from schemas.Sleep import Sleep
from schemas.SleepStatistics import SleepStatistics


class SleepMapper:
    """
    A utility class for mapping Sleep and SleepLevel DTOs into Sleep and SleepStatistics domain models.
    """

    @staticmethod
    def from_sleep(sleep: SleepModel, sleepLevel: SleepLevel, sleepLevelType: str) -> Sleep:
        """
        Maps a SleepLevel and associated Sleep DTO into a Sleep domain model.

        Parameters:
        -----------
        sleep : SleepModel
            The main sleep DTO containing user and summary data.
        sleepLevel : SleepLevel
            A segment of the sleep data representing a specific sleep stage (e.g., deep, light).
        sleepLevelType : str
            The type of sleep level (e.g., "deep", "light", "REM", "awake").

        Returns:
        --------
        Sleep
            A Sleep model representing the sleep level information with calendar metadata.
        """
        start_time_date = datetime.fromtimestamp(sleepLevel.startTimeInSeconds).date()
        week_day = start_time_date.weekday()
        month = start_time_date.month

        return Sleep(
            userId=sleep.userId,
            userAccessToken=sleep.userAccessToken,
            summaryId=sleep.summaryId,
            sleepLevelType=sleepLevelType,
            startTimeOffsetInSeconds=sleepLevel.startTimeInSeconds,
            endTimeOffsetInSeconds=sleepLevel.endTimeInSeconds,
            durationInSeconds=sleep.durationInSeconds,
            validation=sleep.validation,
            calendarDate=start_time_date,
            dayOfWeek=week_day,
            month=month
        )

    @staticmethod
    def to_sleep_stats(sleep: SleepModel) -> SleepStatistics:
        """
        Maps a Sleep DTO into a SleepStatistics domain model, summarizing the entire sleep session.

        Parameters:
        -----------
        sleep : SleepModel
            The sleep DTO containing detailed duration and stage information.

        Returns:
        --------
        SleepStatistics
            A SleepStatistics model containing summarized sleep data and calendar metadata.
        """
        start_time_date = datetime.fromtimestamp(sleep.startTimeInSeconds).date()
        week_day = start_time_date.weekday()
        month = start_time_date.month

        return SleepStatistics(
            userId=sleep.userId,
            userAccessToken=sleep.userAccessToken,
            summaryId=sleep.summaryId,
            startTimeOffsetInSeconds=sleep.startTimeInSeconds,
            durationInSeconds=sleep.durationInSeconds,
            unmeasurableSleepInSeconds=sleep.unmeasurableSleepInSeconds,
            deepSleepDurationInSeconds=sleep.deepSleepDurationInSeconds,
            lightSleepDurationInSeconds=sleep.lightSleepDurationInSeconds,
            remSleepInSeconds=sleep.remSleepInSeconds,
            awakeDurationInSeconds=sleep.awakeDurationInSeconds,
            calendarDate=start_time_date,
            dayOfWeek=week_day,
            month=month
        )

    @staticmethod
    def to_dataframe(data: List[Sleep]) -> DataFrame:
        """
        Converts a list of Sleep entries into a pandas DataFrame.

        Parameters:
        -----------
        data : List[Sleep]

        Returns:
        --------
        DataFrame
        """
        df = pd.DataFrame({
            'timeStart': pd.Series(dtype='int'),
            'timeEnd': pd.Series(dtype='int'),
            'sleepLevelType': pd.Series(dtype='str'),
            'calendarDate': pd.Series(dtype='str'),
            'dayOfWeek': pd.Series(dtype='int'),
            'month': pd.Series(dtype='int')
        })

        df['timeStart'] = [d.startTimeOffsetInSeconds for d in data]
        df['timeEnd'] = [d.endTimeOffsetInSeconds for d in data]
        df['sleepLevelType'] = [d.sleepLevelType for d in data]
        df['calendarDate'] = [d.calendarDate for d in data]
        df['dayOfWeek'] = [d.dayOfWeek for d in data]
        df['month'] = [d.month for d in data]

        df['timeStart'] = pd.to_datetime(df['timeStart'], unit='s')
        df['timeEnd'] = pd.to_datetime(df['timeEnd'], unit='s')
        return df
