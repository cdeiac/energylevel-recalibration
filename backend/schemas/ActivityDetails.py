from pydantic.schema import date
from typing import List
from pydantic import BaseModel
from enums.ActivityType import ActivityType


class ActivityDetail(BaseModel):
    userId: str
    userAccessToken: str
    summaryId: str
    activityId: int
    activityName: str
    activityDescription: str
    durationInSeconds: int
    startTimeInSeconds: int
    startTimeOffsetInSeconds: int
    activityType: ActivityType
    averageHeartRateInBeatsPerMinute: int
    averageRunCadenceInStepsPerMinute: float
    averageSpeedInMetersPerSecond: float
    averagePaceInMinutesPerKilometer: float
    activeKilocalories: int
    distanceInMeters: float
    maxHeartRateInBeatsPerMinute: int
    maxPaceInMinutesPerKilometer: float
    maxRunCadenceInStepsPerMinute: float
    maxSpeedInMetersPerSecond: float
    steps: int
    totalElevationGainInMeters: float
    calendarDate: date
    dayOfWeek: int
    month: int


class ActivityDetails(BaseModel):
    activities: List[ActivityDetail]
