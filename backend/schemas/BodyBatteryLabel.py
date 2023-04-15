from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pydantic.schema import date


class BodyBatteryLabel(BaseModel):
    userId: str
    value: int
    timestamp: int
    calendarDate: date
    dayOfWeek: int
    month: int

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)
