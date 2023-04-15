from datetime import date
from typing import List, Optional, Dict

from pydantic import BaseModel


class StressDetail(BaseModel):
    userId: Optional[str]
    userAccessToken: Optional[str]
    summaryId: str
    startTimeInSeconds: int
    startTimeOffsetInSeconds: int
    durationInSeconds: int
    calendarDate: date
    timeOffsetStressLevelValues: Dict[str, int]
    timeOffsetBodyBatteryValues: Dict[str, int]

    class Settings:
        name = "stress_detail"


class StressDetails(BaseModel):
    stressDetails: List[StressDetail]
