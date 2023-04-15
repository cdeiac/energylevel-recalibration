from typing import List, Dict, Optional
from pydantic import BaseModel


class SleepLevel(BaseModel):
    startTimeInSeconds: int
    endTimeInSeconds: int


class SleepLevelsMap(BaseModel):
    awake: Optional[List[SleepLevel]]
    deep: Optional[List[SleepLevel]]
    light: Optional[List[SleepLevel]]
    rem: Optional[List[SleepLevel]]


class Sleep(BaseModel):
    userId: str
    userAccessToken: str
    summaryId: str
    calendarDate: str
    durationInSeconds: int
    startTimeInSeconds: int
    startTimeOffsetInSeconds: int
    unmeasurableSleepInSeconds: int
    deepSleepDurationInSeconds: int
    lightSleepDurationInSeconds: int
    remSleepInSeconds: int
    awakeDurationInSeconds: int
    sleepLevelsMap: SleepLevelsMap
    validation: str
    timeOffsetSleepSpo2: Dict[str, float]
    timeOffsetSleepRespiration: Dict[str, float] # might be obsolete depending on respiration endpoint

    class Config:
        use_enum_values = True


class Sleeps(BaseModel):
    sleeps: List[Sleep]
