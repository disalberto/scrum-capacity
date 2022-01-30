from enum import IntEnum

"""Module representing the header of the Grid"""


class Columns(IntEnum):
    """
    To associate each member attribute with a table column.
    """

    NAME = 0
    DAYS_OFF = 1
    TRAINING_DAYS = 2
    SUPPORT_DAYS = 3
    ACTIVITY = 4
    CAPACITY = 5
    NOTES = 6
