from datetime import datetime
from dtos.stressdetail import StressDetail
from schemas.stress import StressLevel


class StressLevelMapper:

    def from_stress_detail(stressDetail: StressDetail, offset: str, value: int):
        # format timestamps
        unix_timestamp = stressDetail.startTimeInSeconds + stressDetail.startTimeOffsetInSeconds + int(offset)
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
