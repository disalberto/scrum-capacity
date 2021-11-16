from csv import DictReader
from person import Member

SCRUM_FACTOR=0.8
ROUND_PRECISION=2

def computeCapacity(inputFile: str, sprintDays: str):
    capacity=0
    with open(inputFile, 'r') as read_obj:
        csv_dict_reader = DictReader(read_obj, delimiter = ",")
        for row in csv_dict_reader:
            member = Member(**row)
            mCapa = memberCapacity(member, sprintDays)
            capacity+=mCapa
            print("Team member: " + member.name + " - Capacity in Story Points: " + str(mCapa))
    return round(capacity, ROUND_PRECISION)


def memberCapacity(member: Member, sprintDays: str):
    capa=round(max(0, int(sprintDays) - int(member.daysOff) - int(member.trainingDays)) * int(member.activity) / 100 * SCRUM_FACTOR, ROUND_PRECISION)
    return capa