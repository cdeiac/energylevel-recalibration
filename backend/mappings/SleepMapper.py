from datetime import datetime

from dtos.sleep import Sleep as SleepModel, SleepLevel
from schemas.Sleep import Sleep
from schemas.SleepStatistics import SleepStatistics


class SleepMapper:

    @staticmethod
    def from_sleep(sleep: SleepModel, sleepLevel: SleepLevel, sleepLevelType: str):
        # format offset timestamps
        offset_start_time = sleepLevel.startTimeInSeconds + sleep.startTimeOffsetInSeconds
        offset_end_time = sleepLevel.endTimeInSeconds + sleep.startTimeOffsetInSeconds
        offset_start_time_date = datetime.fromtimestamp(offset_start_time).date()
        week_day = offset_start_time_date.weekday()
        month = offset_start_time_date.month

        return Sleep(
            userId=sleep.userId,
            userAccessToken=sleep.userAccessToken,
            summaryId=sleep.summaryId,
            sleepLevelType=sleepLevelType,
            startTimeOffsetInSeconds=offset_start_time,
            endTimeOffsetInSeconds=offset_end_time,
            durationInSeconds=sleep.durationInSeconds,
            validation=sleep.validation,
            calendarDate=offset_start_time_date,
            dayOfWeek=week_day,
            month=month
        )

    @staticmethod
    def to_sleep_stats(sleep: SleepModel):
        # format offset timestamps
        offset_start_time = sleep.startTimeInSeconds + sleep.startTimeOffsetInSeconds
        offset_start_time_date = datetime.fromtimestamp(offset_start_time).date()
        week_day = offset_start_time_date.weekday()
        month = offset_start_time_date.month

        return SleepStatistics(
            userId=sleep.userId,
            userAccessToken=sleep.userAccessToken,
            summaryId=sleep.summaryId,
            startTimeOffsetInSeconds=offset_start_time,
            durationInSeconds=sleep.durationInSeconds,
            unmeasurableSleepInSeconds=sleep.unmeasurableSleepInSeconds,
            deepSleepDurationInSeconds=sleep.deepSleepDurationInSeconds,
            lightSleepDurationInSeconds=sleep.lightSleepDurationInSeconds,
            remSleepInSeconds=sleep.remSleepInSeconds,
            awakeDurationInSeconds=sleep.awakeDurationInSeconds,
            calendarDate=offset_start_time_date,
            dayOfWeek=week_day,
            month=month
        )
