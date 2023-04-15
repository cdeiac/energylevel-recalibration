from typing import Optional

from pydantic.schema import date

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

class Sleep(BaseModel):
    userId: str
    userAccessToken: str
    summaryId: str
    calendarDate: date
    sleepLevelType: str
    startTimeOffsetInSeconds: int
    endTimeOffsetInSeconds: int
    durationInSeconds: int
    validation: str
    dayOfWeek: int
    month: int
    timestamp: Optional[int] # only used for resampling

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

    class Config:
        exclude = {'timestamp'}
