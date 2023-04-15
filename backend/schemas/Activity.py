from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pydantic.types import date

from enums.ActivityType import ActivityType


class Activity(BaseModel):
    userId: str
    userAccessToken: str
    summaryId: str
    activityId: int
    activityName: str
    activityDescription: str
    durationInSeconds: int
    activityType: ActivityType
    startTimeOffsetInSeconds: int
    endTimeOffsetInSeconds: int
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
    timestamp: Optional[int]  # only used for resampling

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

    class Config:
        exclude = {'timestamp'}


class Activities(BaseModel):
    activities: List[Activity]