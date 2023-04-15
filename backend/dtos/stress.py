from typing import List
from pydantic import BaseModel

from dtos.stressdetail import StressDetail


class Stress(BaseModel):
    __root__: List[StressDetail]
