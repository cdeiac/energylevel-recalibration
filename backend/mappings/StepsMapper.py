from datetime import datetime

from schemas.Activity import Activity
from schemas.Steps import Steps


class StepsMapper:

    @staticmethod
    def from_activity(activity: Activity) -> Steps:
        # startTimeOffsetInSeconds is already an offset timestamp
        date = datetime.fromtimestamp(activity.startTimeOffsetInSeconds).date()
        day_of_week = date.weekday()
        month = date.month

        return Steps(
            userId=activity.userId,
            userAccessToken=activity.userAccessToken,
            summaryId=activity.summaryId,
            activityId= activity.activityId,
            value=activity.steps,
            calendarDate=date,
            dayOfWeek=day_of_week,
            month=month,
            timestamp=activity.timestamp
        )
