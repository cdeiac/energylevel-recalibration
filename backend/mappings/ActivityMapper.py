from datetime import datetime

from dtos.Activity import Activity as ActivityDTO
from enums.ActivityType import ActivityType
from schemas.Activity import Activity


class ActivityMapper:

    def from_activity(activity: ActivityDTO):
        # format timestamp and offsets
        offset_start_time = activity.startTimeInSeconds + activity.startTimeOffsetInSeconds
        offset_end_time = offset_start_time + activity.durationInSeconds
        date = datetime.fromtimestamp(offset_start_time).date()
        day_of_week = date.weekday()
        month = date.month

        return Activity(
            userId=activity.userId,
            userAccessToken=activity.userAccessToken,
            summaryId=activity.summaryId,
            activityId= activity.activityId,
            activityName=activity.activityName,
            activityDescription=activity.activityDescription,
            durationInSeconds=activity.durationInSeconds,
            startTimeOffsetInSeconds=offset_start_time,
            endTimeOffsetInSeconds=offset_end_time,
            activityType=ActivityType[activity.activityType],
            averageHeartRateInBeatsPerMinute=activity.averageHeartRateInBeatsPerMinute,
            averageRunCadenceInStepsPerMinute=activity.averageRunCadenceInStepsPerMinute,
            averageSpeedInMetersPerSecond=activity.averageSpeedInMetersPerSecond,
            averagePaceInMinutesPerKilometer=activity.averagePaceInMinutesPerKilometer,
            activeKilocalories=activity.activeKilocalories,
            distanceInMeters=activity.distanceInMeters,
            maxHeartRateInBeatsPerMinute=activity.maxHeartRateInBeatsPerMinute,
            maxPaceInMinutesPerKilometer=activity.maxPaceInMinutesPerKilometer,
            maxRunCadenceInStepsPerMinute=activity.maxRunCadenceInStepsPerMinute,
            maxSpeedInMetersPerSecond=activity.maxSpeedInMetersPerSecond,
            steps=activity.steps,
            totalElevationGainInMeters=activity.totalElevationGainInMeters,
            calendarDate=date,
            dayOfWeek=day_of_week,
            month=month
        )
