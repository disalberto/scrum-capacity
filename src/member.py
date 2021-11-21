from typing import List
from pydantic import BaseModel
from enum import IntEnum

class Member(BaseModel):
    name: str
    days_off: int
    training_days: int
    activity: int

    def set_value(self, pos: int, value: str):
        if pos == int(Columns.NAME):
            self.name = value
        elif pos == int(Columns.DAYS_OFF):
            self.days_off = int(value)
        elif pos == int(Columns.TRAINING_DAYS):
            self.training_days = int(value)
        elif pos == int(Columns.ACTIVITY):
            self.activity = int(value)
        else:
            raise Exception('Unhandled column')

class MemberList(BaseModel):
    __root__: List[Member]

class Columns(IntEnum):
    NAME = 0
    DAYS_OFF = 1
    TRAINING_DAYS = 2
    ACTIVITY = 3