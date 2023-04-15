from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pydantic.schema import date


class Respiration(BaseModel):
    timestamp: int
    dataType: str = 'stress'
    value: float
    # additional fields
    userId: str
    userAccessToken: str
    summaryId: str
    durationInSeconds: int
    calendarDate: date
    dayOfWeek: int
    month: int

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)
