from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


class DailySummary(BaseModel):
    summaryId: str
    calendarDate: str
    activityType: str
    activeKilocalories: int
    bmrKilocalories: int
    steps: int
    distanceInMeters: float
    durationInSeconds: int
    activeTimeInSeconds: int
    startTimeInSeconds: int
    startTimeOffsetInSeconds: int
    moderateIntensityDurationInSeconds: int
    vigorousIntensityDurationInSeconds: int
    floorsClimbed: int
    minHeartRateInBeatsPerMinute: int
    averageHeartRateInBeatsPerMinute: int
    maxHeartRateInBeatsPerMinute: int
    timeOffsetHeartRateSamples: dict
    averageStressLevel: int
    maxStressLevel: int
    stressDurationInSeconds: int
    restStressDurationInSeconds: int
    activityStressDurationInSeconds: int
    lowStressDurationInSeconds: int
    mediumStressDurationInSeconds: int
    highStressDurationInSeconds: int
    stressQualifier: str
    stepsGoal: int
    intensityDurationGoalInSeconds: int
    floorsClimbedGoal: int

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)
