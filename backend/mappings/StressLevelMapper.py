from datetime import datetime
from typing import List

import pandas as pd
from pandas import DataFrame

from dtos.stressdetail import StressDetail
from schemas.stress import StressLevel


class StressLevelMapper:
    """
    A utility class for mapping StressDetail DTOs into StressLevel domain models.
    """

    @staticmethod
    def from_stress_detail(stressDetail: StressDetail, offset: str, value: int) -> StressLevel:
        """
        Converts a StressDetail DTO into a StressLevel domain model.

        Computes the timestamp by adding an offset (in seconds) to the DTO's
        `startTimeInSeconds`, then derives calendar metadata.

        Parameters:
        -----------
        stressDetail : StressDetail
            The data transfer object containing stress event information.
        offset : str
            The offset in seconds (as a string) to apply to `startTimeInSeconds`.
        value : int
            The numeric stress level value to associate with the measurement.

        Returns:
        --------
        StressLevel
            A populated StressLevel domain model with timestamp and calendar fields.
        """
        unix_timestamp = stressDetail.startTimeInSeconds + int(offset)
        date = datetime.fromtimestamp(unix_timestamp).date()
        day_of_week = date.weekday()
        month = date.month

        return StressLevel(
            timestamp=unix_timestamp,
            value=value,
            userId=stressDetail.userId,
            userAccessToken=stressDetail.userAccessToken,
            summaryId=stressDetail.summaryId,
            durationInSeconds=stressDetail.durationInSeconds,
            calendarDate=date,
            dayOfWeek=day_of_week,
            month=month
        )

    @staticmethod
    def to_dataframe(data: List[StressLevel]) -> DataFrame:
        """
        Converts a list of StressLevel objects into a pandas DataFrame.

        Parameters:
        -----------
        data : List[StressLevel]
            Parsed list of stress level schema objects.

        Returns:
        --------
        DataFrame
            Tabular structure for analysis or modeling.
        """
        df = pd.DataFrame({
            'timestamp': pd.Series(dtype='int'),
            'stressLevel': pd.Series(dtype='int'),
            'calendarDate': pd.Series(dtype='str'),
            'dayOfWeek': pd.Series(dtype='int'),
            'month': pd.Series(dtype='int')
        })

        df['stressLevel'] = [d.value for d in data]
        df['timestamp'] = [d.timestamp for d in data]
        df['calendarDate'] = [d.calendarDate for d in data]
        df['dayOfWeek'] = [d.dayOfWeek for d in data]
        df['month'] = [d.month for d in data]

        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        return df
