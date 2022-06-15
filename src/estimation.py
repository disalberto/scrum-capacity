# pylint: disable=too-few-public-methods
# pylint: disable=no-name-in-module

from datetime import date
from typing import Optional
from pydantic import BaseModel
from member import MemberList


class Estimation(BaseModel):
    """Class representing the estimation"""

    date_from: date
    date_to: date
    sprint_days: int
    scrum_factor: int
    capacity: float

    committed_sp: Optional[int]
    delivered_sp: Optional[int]

    member_list: MemberList
