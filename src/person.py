from dataclasses import dataclass

@dataclass
class Member:
    name: str
    daysOff: int
    trainingDays: int
    activity: int