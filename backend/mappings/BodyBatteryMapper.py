from datetime import datetime

from dtos.stressdetail import StressDetail
from schemas.bodyBattery import BodyBattery


class BodyBatteryMapper:

    def from_stress_detail(stressDetail: StressDetail, offset: str, value: int):
        # format timestamps
        unix_timestamp = stressDetail.startTimeInSeconds + stressDetail.startTimeOffsetInSeconds + int(offset)
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
