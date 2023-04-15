from datetime import date
from typing import Optional, Dict, List

from pydantic import BaseModel


class RespirationDetail(BaseModel):
    userId: Optional[str]
    userAccessToken: Optional[str]
    summaryId: str
    startTimeInSeconds: int
    startTimeOffsetInSeconds: int
    durationInSeconds: int
    #calendarDate: date
    timeOffsetEpochToBreaths: Dict[str, float]

    class Settings:
        name = "respiration"


class RespirationDetails(BaseModel):
    allDayRespiration: List[RespirationDetail] # allDayRespiration
