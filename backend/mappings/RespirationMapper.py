from datetime import datetime, timedelta

from dtos.respirationdetail import RespirationDetail
from schemas.Respiration import Respiration


class RespirationMapper:

    def from_respiration_detail(respirationDetail: RespirationDetail, timestamp: str, value: int):
        # format timestamps
        offset_timestamp = int(respirationDetail.startTimeInSeconds) + int(respirationDetail.startTimeOffsetInSeconds)
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
