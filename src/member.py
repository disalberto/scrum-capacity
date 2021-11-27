from typing import List
from pydantic import BaseModel
from column import Columns

class Member(BaseModel):
    """
    Class Member representing team member.
    He/she has a name, a number of days off, a number of training days and an activity % (0-100)
    """
    name: str
    days_off: int
    training_days: int
    activity: int

    def set_value(self, pos: int, value: str):
        """
        Method to update a member after he has been modified in the main table.
        The if-else statement is used to identify which attribute to modify
        with the given value.
        :param pos: position in the table (column).
        :param value: value in the modified cell.
        :return: nothing.
        """
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
    """
    Class representing a list of Member.
    """
    __root__: List[Member]
