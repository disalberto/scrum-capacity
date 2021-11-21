from csv import DictReader
from member import Member, MemberList

SCRUM_FACTOR=0.8
ROUND_PRECISION=2

def compute_capacity(mList: MemberList, sprint_days: str):
    """
    For each member of the list and given a certain amount of days in the sprint,
    It returns the total capacity of the team, with a given round precision
    :param mList: the input MemberList
    :param sprint_days: number of days in the iteration
    :return: the total capacity
    """
    capacity=0

    for member in mList:
        m_capa = member_capacity(member, sprint_days)
        capacity += m_capa

    return round(capacity, ROUND_PRECISION)


def member_capacity(member: Member, sprint_days: str):
    """
    Method to compute the capacity of a person for a given sprint
    :param member: a given team member
    :param sprint_days: the number of days in the sprint
    :return: his/her capacity
    """
    capa=round(max(0, int(sprint_days) - member.days_off - member.training_days)
               * member.activity / 100 * SCRUM_FACTOR, ROUND_PRECISION)
    return capa