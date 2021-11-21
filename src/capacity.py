from csv import DictReader
from member import Member, MemberList

SCRUM_FACTOR=0.8
ROUND_PRECISION=2

def compute_capacity(mList: MemberList, sprint_days: str):
    capacity=0

    for member in mList:
        m_capa = member_capacity(member, sprint_days)
        capacity += m_capa

    return round(capacity, ROUND_PRECISION)


def member_capacity(member: Member, sprint_days: str):
    capa=round(max(0, int(sprint_days) - member.days_off - member.training_days) * member.activity / 100 * SCRUM_FACTOR, ROUND_PRECISION)
    return capa