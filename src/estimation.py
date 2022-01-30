# pylint: disable=too-few-public-methods
# pylint: disable=no-name-in-module

from pydantic import BaseModel
from member import MemberList


class Estimation(BaseModel):
    """Class representing the estimation"""

    date_from: str
    date_to: str
    sprint_days: float
    scrum_factor: float
    capacity: float

    member_list: MemberList
