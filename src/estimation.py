from pydantic import BaseModel
from member import MemberList

"""Module representing an estimation"""


class Estimation(BaseModel):
    date_from: str
    date_to: str
    sprint_days: float
    scrum_factor: float
    capacity: float

    member_list: MemberList
