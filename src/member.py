from typing import List
from pydantic import BaseModel
from enum import IntEnum

class Member(BaseModel):
    name: str
    daysOff: int
    trainingDays: int
    activity: int

class MemberList(BaseModel):
    __root__: List[Member]

class Columns(IntEnum):
    NAME = 0
    DAYS_OFF = 1
    TRAINING_DAYS = 2
    ACTIVITY = 3