from pydantic import Field
from pydantic.main import BaseModel

from schemas import PyObjectId


class User(BaseModel):
    id: str = Field(default_factory=PyObjectId, alias="_id")
    userId: str = Field(...)
    userAccessToken: str = Field(...)
