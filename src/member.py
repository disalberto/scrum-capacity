# pylint: disable=no-name-in-module

from typing import List
from pydantic import BaseModel
from column import TeamColumns


class Member(BaseModel):
    """
    Class Member representing team member.
    He/she has a name, a number of days off, a number of training days and an activity % (0-100)
    """

    name: str
    days_off: float
    training_days: float
    support_days: float
    activity: float
    capacity: float
    notes: str

    def set_value(self, pos: int, value: str):
        """
        Method to update a member after he has been modified in the main table
        The if-else statement is used to identify which attribute to modify
        with the given value
        :param pos: position in the table (column)
        :param value: value in the modified cell
        :return: nothing
        """
        if pos == int(TeamColumns.NAME.index):
            self.name = value
        elif pos == int(TeamColumns.DAYS_OFF.index):
            self.days_off = float(value)
        elif pos == int(TeamColumns.TRAINING_DAYS.index):
            self.training_days = float(value)
        elif pos == int(TeamColumns.SUPPORT_DAYS.index):
            self.support_days = float(value)
        elif pos == int(TeamColumns.ACTIVITY.index):
            self.activity = float(value)
        elif pos == int(TeamColumns.CAPACITY.index):
            self.capacity = float(value)
        elif pos == int(TeamColumns.NOTES.index):
            self.notes = value
        else:
            raise Exception("Unhandled column")

    def get_value(self, pos: int):
        """
        Method to get the value of the attribute of the corresponding column
        :param pos: position in the table (column)
        :return: the attribute's value
        """
        if pos == int(TeamColumns.NAME.index):
            ret = self.name
        elif pos == int(TeamColumns.DAYS_OFF.index):
            ret = str(self.days_off)
        elif pos == int(TeamColumns.TRAINING_DAYS.index):
            ret = str(self.training_days)
        elif pos == int(TeamColumns.SUPPORT_DAYS.index):
            ret = str(self.support_days)
        elif pos == int(TeamColumns.ACTIVITY.index):
            ret = str(self.activity)
        elif pos == int(TeamColumns.NOTES.index):
            ret = self.notes
        else:
            raise Exception("Unhandled column")

        return ret


class MemberList(BaseModel):
    """
    Class representing a list of Member.
    """

    __root__: List[Member]
