from csv import DictReader
from member import Member, MemberList

SCRUM_FACTOR=0.8
ROUND_PRECISION=2

def compute_capacity(mList: MemberList, sprintDays: str):
    capacity=0

    for member in mList:
        mCapa = member_capacity(member, sprintDays)
        capacity+=mCapa
            #print("Team member: " + member.name + " - Capacity in Story Points: " + str(mCapa))
    return round(capacity, ROUND_PRECISION)


def member_capacity(member: Member, sprintDays: str):
    capa=round(max(0, int(sprintDays) - member.daysOff - member.trainingDays) * member.activity / 100 * SCRUM_FACTOR, ROUND_PRECISION)
    return capa