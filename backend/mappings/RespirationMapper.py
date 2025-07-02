from datetime import datetime
from typing import List

import pandas as pd
from pandas import DataFrame

from dtos.respirationdetail import RespirationDetail
from schemas.Respiration import Respiration


class RespirationMapper:
    """
    A utility class for mapping RespirationDetail DTOs into Respiration domain models.
    """

    @staticmethod
    def from_respiration_detail(respirationDetail: RespirationDetail, timestamp: str, value: int) -> Respiration:
        """
        Converts a RespirationDetail DTO into a Respiration domain model instance.

        Computes the absolute timestamp using the provided `timestamp` offset
        and the `startTimeInSeconds` from the DTO, then extracts calendar details.

        Parameters:
        -----------
        respirationDetail : RespirationDetail
            The DTO containing respiration data.
        timestamp : str
            A string offset (in seconds) to be added to `startTimeInSeconds`.
        value : int
            The respiration value to assign to the resulting model.

        Returns:
        --------
        Respiration
            A fully populated Respiration model instance with timestamp and date metadata.
        """
        offset_timestamp = int(respirationDetail.startTimeInSeconds)
        unix_timestamp = offset_timestamp + int(timestamp)
        date = datetime.fromtimestamp(unix_timestamp).date()
        day_of_week = date.weekday()
        month = date.month

        return Respiration(
            timestamp=unix_timestamp,
            value=value,
            userId=respirationDetail.userId,
            userAccessToken=respirationDetail.userAccessToken,
            summaryId=respirationDetail.summaryId,
            durationInSeconds=respirationDetail.durationInSeconds,
            calendarDate=date,
            dayOfWeek=day_of_week,
            month=month
        )

    @staticmethod
    def to_dataframe(data: List[Respiration]) -> DataFrame:
        """
                Converts a list of Respiration objects into a pandas DataFrame.

                Parameters:
                -----------
                data : List[Respiration]
                    A list of respiration domain objects.

                Returns:
                --------
                DataFrame
                    A structured DataFrame suitable for analysis or modeling.
                """
        df = pd.DataFrame({
            'summaryId': pd.Series(dtype='str'),
            'timestamp': pd.Series(dtype='int'),
            'respiration': pd.Series(dtype='int'),
            'calendarDate': pd.Series(dtype='str'),
            'dayOfWeek': pd.Series(dtype='int'),
            'month': pd.Series(dtype='int')
        })

        df['summaryId'] = [d.summaryId for d in data]
        df['timestamp'] = [d.timestamp for d in data]
        df['respiration'] = [d.value for d in data]
        df['calendarDate'] = [d.calendarDate for d in data]
        df['dayOfWeek'] = [d.dayOfWeek for d in data]
        df['month'] = [d.month for d in data]

        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        return df