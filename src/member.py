from typing import List
from pydantic import BaseModel
from column import Columns


class Member(BaseModel):
    """
    Class Member representing team member.
    He/she has a name, a number of days off, a number of training days and an activity % (0-100)
    """
    name: str
    days_off: float
    training_days: float
    activity: float
    capacity: float

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
            self.days_off = float(value)
        elif pos == int(Columns.TRAINING_DAYS):
            self.training_days = float(value)
        elif pos == int(Columns.ACTIVITY):
            self.activity = float(value)
        elif pos == int(Columns.CAPACITY):
            self.capacity = float(value)
        else:
            raise Exception('Unhandled column')

    def get_value(self, pos: int):
        """
        Method to get the value of the attribute of the corresponding column.
        :param pos: position in the table (column).
        :return: the attribute's value.
        """
        if pos == int(Columns.NAME):
            ret = self.name
        elif pos == int(Columns.DAYS_OFF):
            ret = str(self.days_off)
        elif pos == int(Columns.TRAINING_DAYS):
            ret = str(self.training_days)
        elif pos == int(Columns.ACTIVITY):
            ret = str(self.activity)
        else:
            raise Exception('Unhandled column')

        return ret


class MemberList(BaseModel):
    """
    Class representing a list of Member.
    """
    __root__: List[Member]
