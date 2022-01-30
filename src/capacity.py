from multipledispatch import dispatch
from member import Member, MemberList

"""Module to compute the capacity"""

ROUND_PRECISION = 2


@dispatch(list)
def compute_capacity(mList: MemberList):
    """
    For each member of the list,
    it returns the total capacity of the team, with a given round precision
    :param mList: the input MemberList
    :return: the total capacity
    """
    capacity: float = 0.0

    for member in mList:
        capacity += member.capacity

    return round(capacity, ROUND_PRECISION)


@dispatch(list, float, float)
def compute_capacity(mList: MemberList, sprint_days: float, scrum_factor: float):
    """
    For each member of the list and given a certain amount of days in the sprint,
    It returns the total capacity of the team, with a given round precision
    :param mList: the input MemberList
    :param sprint_days: number of days in the iteration
    :param scrum_factor: the % of time spent in SCRUM activities
    :return: the total capacity
    """
    capacity = 0

    for member in mList:
        m_capa = member_capacity(member, sprint_days, scrum_factor)
        capacity += m_capa

    return round(capacity, ROUND_PRECISION)


def member_capacity(member: Member, sprint_days: float, scrum_factor: float):
    """
    Method to compute the capacity of a person for a given sprint
    :param member: a given team member
    :param sprint_days: the number of days in the sprint
    :param scrum_factor: the % of time spent in SCRUM activities
    :return: his/her capacity
    """
    effectiveness: float = 100.0 - float(scrum_factor)
    capa = round(
        max(
            0.0,
            sprint_days - member.days_off - member.training_days - member.support_days,
        )
        * member.activity
        * effectiveness
        / 10000,
        ROUND_PRECISION,
    )
    return capa
