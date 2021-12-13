from pydantic import BaseModel
from member import MemberList


class Estimation(BaseModel):
    sprint_days: float
    scrum_factor: float
    capacity: float

    member_list: MemberList
