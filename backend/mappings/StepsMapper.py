from datetime import datetime
from typing import List

import pandas as pd
from pandas import DataFrame, Series

from schemas.Activity import Activity
from schemas.Steps import Steps


class StepsMapper:
    """
    A utility class for mapping Activity domain models into Steps domain models.
    """

    @staticmethod
    def from_activity(activity: Activity) -> Steps:
        """
        Converts an Activity instance into a Steps model.

        Extracts step-related data from the Activity model and enriches it with
        calendar metadata (date, weekday, and month) derived from the activity's
        start time.

        Parameters:
        -----------
        activity : Activity
            The Activity domain model containing step count and timestamp information.

        Returns:
        --------
        Steps
            A Steps domain model populated with data derived from the Activity instance.
        """
        date = datetime.fromtimestamp(activity.startTimeOffsetInSeconds).date()
        day_of_week = date.weekday()
        month = date.month

        return Steps(
            userId=activity.userId,
            userAccessToken=activity.userAccessToken,
            summaryId=activity.summaryId,
            activityId=activity.activityId,
            value=activity.steps,
            calendarDate=date,
            dayOfWeek=day_of_week,
            month=month,
            timestamp=activity.timestamp
        )

    @staticmethod
    def to_dataframe(data: List[Steps]) -> DataFrame:
        """
                Converts a list of Steps objects into a pandas DataFrame.

                Parameters:
                -----------
                data : List[Steps]
                    A list of Steps schema objects.

                Returns:
                --------
                DataFrame
                    A DataFrame containing step values and metadata.
                """
        df = DataFrame({
            'summaryId': Series(dtype='str'),
            'timestamp': Series(dtype='int'),
            'steps': Series(dtype='int'),
            'calendarDate': Series(dtype='str'),
            'dayOfWeek': Series(dtype='int'),
            'month': Series(dtype='int')
        })

        df['summaryId'] = [d.summaryId for d in data]
        df['timestamp'] = [d.timestamp for d in data]
        df['value'] = [d.value for d in data]  # likely should be 'steps' instead of 'value'

        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        return df