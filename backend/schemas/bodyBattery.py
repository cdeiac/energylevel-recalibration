from typing import Optional

from fastapi.encoders import jsonable_encoder
from pydantic import validator
from pydantic.main import BaseModel, Field
from pydantic.schema import datetime, date


class BodyBattery(BaseModel):
    dataType: str = 'bodyBattery'
    value: int
    label: Optional[int] = None
    # additional fields
    userId: Optional[str] = None
    userAccessToken: Optional[str] = None
    summaryId: str
    timestamp: int
    durationInSeconds: int
    calendarDate: date
    dayOfWeek: int
    month: int

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        orm_mode = True
        json_encoders = {
            #datetime: lambda dt: dt.astimezone(pytz.utc)
        }

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)
