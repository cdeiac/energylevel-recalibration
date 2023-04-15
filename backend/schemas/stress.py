from pydantic.schema import date
from typing import Optional

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


class StressLevel(BaseModel):
    timestamp: int
    dataType: str = 'stress'
    value: int
    # additional fields
    userId: Optional[str] = None
    userAccessToken: Optional[str] = None
    summaryId: str
    durationInSeconds: int
    calendarDate: date
    dayOfWeek: int
    month: int

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)
