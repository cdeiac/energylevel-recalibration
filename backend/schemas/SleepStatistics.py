from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pydantic.schema import date


class SleepStatistics(BaseModel):
    userId: str
    userAccessToken: str
    summaryId: str
    calendarDate: date
    durationInSeconds: int
    startTimeOffsetInSeconds: int
    unmeasurableSleepInSeconds: int
    deepSleepDurationInSeconds: int
    lightSleepDurationInSeconds: int
    remSleepInSeconds: int
    awakeDurationInSeconds: int

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)
