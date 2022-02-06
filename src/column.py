from enum import Enum


class BaseColumns(Enum):
    """
    Base Enum with label
    """

    def __init__(self, index, label):
        self.index = index
        self.label = label


class TeamColumns(BaseColumns):
    """
    To associate each member attribute with a table column.
    """

    NAME = 0, "Name"
    DAYS_OFF = 1, "Days Off"
    TRAINING_DAYS = 2, "Training Days"
    SUPPORT_DAYS = 3, "Support Days"
    ACTIVITY = 4, "Activity in %"
    CAPACITY = 5, "Individual Capacity"
    NOTES = 6, "Notes"


class VelocityColumns(BaseColumns):
    """
    To give a header to the table of previous iterations
    """

    ITN1 = 1, "Iteration N-1"
    ITN2 = 2, "Iteration N-2"
    ITN3 = 3, "Iteration N-3"
