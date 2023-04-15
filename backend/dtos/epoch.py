from typing import List
from pydantic import BaseModel, Field


class EpochEntry(BaseModel):
    userId: str
    userAccessToken: str
    summaryId: str
    activityType: str
    activeKilocalories: int
    steps: int
    distanceInMeters: float
    durationInSeconds: int
    activeTimeInSeconds: int
    startTimeInSeconds: int
    startTimeOffsetInSeconds: int
    met: float
    intensity: str
    meanMotionIntensity: int
    maxMotionIntensity: int


class Epochs(BaseModel):
    __root__: List[EpochEntry]
