from pydantic import BaseModel


class BodyBatteryLabel(BaseModel):
    timestamp: str
    label: int
