from typing import Dict

from pydantic import BaseModel, Field

from schemas import PyObjectId


class StressDetailSchema(BaseModel):
    id: str = Field(default_factory=PyObjectId, alias="_id")
    userId: str = Field(...)
    userAccessToken: str = Field(...)
    summaryId: str = Field(...)
    startTimeInSeconds: int = Field(...)
    startTimeOffsetInSeconds: int = Field(...)
    durationInSeconds: int = Field(...)
    calendarDate: str = Field(...)
    timeOffsetStressLevelValues: Dict[str, int] = Field(...)
    timeOffsetBodyBatteryValues: Dict[str, int] = Field(...)
