from csv import DictReader
from dataclasses import dataclass

SPRINT_DAYS=14
SCRUM_FACTOR=0.8
ROUND_PRECISION=2

@dataclass
class Member:
    name: str
    daysOff: int
    trainingDays: int
    activity: int


def computeCapacity(inputFile):
    capacity=0
    with open(inputFile, 'r') as read_obj:
        csv_dict_reader = DictReader(read_obj, delimiter = ",")
        for row in csv_dict_reader:
            member = Member(**row)
            mCapa = memberCapacity(member)
            capacity+=mCapa
            print("Team member: " + member.name + " - Capacity in Story Points: " + str(mCapa))
    return round(capacity, ROUND_PRECISION)


def memberCapacity(member: Member):
    capa=round(max(0, SPRINT_DAYS - int(member.daysOff) - int(member.trainingDays)) * int(member.activity) / 100 * SCRUM_FACTOR, ROUND_PRECISION)
    return capa