from typing import List, Optional

from pydantic import BaseModel

from dtos.epoch import Epochs
from dtos.stress import Stress


#dailies, thirdPartyDailies, epochs, sleeps, bodyComps, stress, userMetrics, pulseOx, respiration, healthSnapshot, hrv, bloodPressures
class PushNotification(BaseModel):
    epochs: Optional[List[Epochs]] = None
    stress: Optional[List[Stress]] = None
