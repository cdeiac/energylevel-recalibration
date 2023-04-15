from pydantic.schema import date

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


class Steps(BaseModel):
    userId: str
    userAccessToken: str
    summaryId: str
    activityId: str
    calendarDate: date
    dayOfWeek: int
    month: int
    timestamp: int
    value: int

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)
