from datetime import datetime
from typing import List

import pandas as pd
from pandas import DataFrame

from dtos.stressdetail import StressDetail
from schemas.bodyBattery import BodyBattery


class BodyBatteryMapper:
    """
    A utility class for mapping StressDetail DTOs into BodyBattery domain models.
    """

    @staticmethod
    def from_stress_detail(stressDetail: StressDetail, offset: str, value: int) -> BodyBattery:
        """
        Converts a StressDetail DTO into a BodyBattery domain model instance.

        This method computes the effective timestamp by applying the offset to
        the start time and derives additional calendar metadata.

        Parameters:
        -----------
        stressDetail : StressDetail
            The DTO containing stress data from which to extract body battery info.
        offset : str
            A string representing the offset (in seconds) to be added to the start time.
        value : int
            The battery value to assign to the BodyBattery instance.

        Returns:
        --------
        BodyBattery
            A populated BodyBattery model with timestamps and contextual calendar fields.
        """
        unix_timestamp = stressDetail.startTimeInSeconds + int(offset)
        date = datetime.fromtimestamp(unix_timestamp).date()
        day_of_week = date.weekday()
        month = date.month

        return BodyBattery(
            value=value,
            userId=stressDetail.userId,
            userAccessToken=stressDetail.userAccessToken,
            summaryId=stressDetail.summaryId,
            timestamp=unix_timestamp,
            durationInSeconds=stressDetail.durationInSeconds,
            calendarDate=date,
            dayOfWeek=day_of_week,
            month=month
        )

    @staticmethod
    def to_dataframe(data: List[BodyBattery]) -> DataFrame:
        """
        Converts a list of BodyBattery objects into a pandas DataFrame
        Parameters:
        -----------
        data : List[BodyBattery]
            A list of body battery schema objects
        Returns:
        --------
        DataFrame
            A structured DataFrame with relevant fields.
        """
        df = pd.DataFrame({
            'timestamp': pd.Series(dtype='int'),
            'bodyBattery': pd.Series(dtype='int'),
            'calendarDate': pd.Series(dtype='str'),
            'dayOfWeek': pd.Series(dtype='int'),
            'month': pd.Series(dtype='int')})

        df['bodyBattery'] = [d.value for d in data]
        df['timestamp'] = [d.timestamp for d in data]
        df['calendarDate'] = [d.calendarDate for d in data]
        df['dayOfWeek'] = [d.dayOfWeek for d in data]
        df['month'] = [d.month for d in data]

        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        return df
