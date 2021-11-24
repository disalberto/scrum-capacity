from csv import DictReader
from member import Member, MemberList

ROUND_PRECISION=2

def compute_capacity(mList: MemberList, sprint_days: str, scrum_factor: str):
    """
    For each member of the list and given a certain amount of days in the sprint,
    It returns the total capacity of the team, with a given round precision
    :param mList: the input MemberList
    :param sprint_days: number of days in the iteration
    :param scrum_factor: the % of time spent in SCRUM activities
    :return: the total capacity
    """
    capacity=0

    for member in mList:
        m_capa = member_capacity(member, sprint_days, scrum_factor)
        capacity += m_capa

    return round(capacity, ROUND_PRECISION)


def member_capacity(member: Member, sprint_days: str, scrum_factor: str):
    """
    Method to compute the capacity of a person for a given sprint
    :param member: a given team member
    :param sprint_days: the number of days in the sprint
    :param scrum_factor: the % of time spent in SCRUM activities
    :return: his/her capacity
    """
    capa=round(max(0, int(sprint_days) - member.days_off - member.training_days)
               * member.activity * scrum_factor / 10000, ROUND_PRECISION)
    return capa