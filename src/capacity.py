# pylint: disable=function-redefined

from multipledispatch import dispatch
import member

ROUND_PRECISION = 2


@dispatch(list)
def compute_capacity(m_list: member.MemberList):
    """
    For each member of the list,
    it returns the total capacity of the team, with a given round precision
    :param m_list: the input MemberList
    :return: the total capacity
    """
    capacity: float = 0.0

    for mbr in m_list:
        capacity += mbr.capacity

    return round(capacity, ROUND_PRECISION)


@dispatch(list, float, float)
def compute_capacity(
    m_list: member.MemberList, sprint_days: float, scrum_factor: float
):
    """
    For each member of the list and given a certain amount of days in the sprint,
    It returns the total capacity of the team, with a given round precision
    :param m_list: the input MemberList
    :param sprint_days: number of days in the iteration
    :param scrum_factor: the % of time spent in SCRUM activities
    :return: the total capacity
    """
    capacity = 0

    for mbr in m_list:
        m_capa = member_capacity(mbr, sprint_days, scrum_factor)
        capacity += m_capa

    return round(capacity, ROUND_PRECISION)


def member_capacity(mbr: member.Member, sprint_days: float, scrum_factor: float):
    """
    Method to compute the capacity of a person for a given sprint
    :param mbr: a given team member
    :param sprint_days: the number of days in the sprint
    :param scrum_factor: the % of time spent in SCRUM activities
    :return: his/her capacity
    """
    effectiveness: float = 100.0 - float(scrum_factor)
    capa = round(
        max(
            0.0,
            sprint_days - mbr.days_off - mbr.training_days - mbr.support_days,
        )
        * mbr.activity
        * effectiveness
        / 10000,
        ROUND_PRECISION,
    )
    return capa
