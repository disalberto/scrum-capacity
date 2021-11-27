from pydantic import BaseModel
from member import MemberList

class Estimation(BaseModel):

    sprint_days: int
    scrum_factor: int
    capacity: float

    member_list: MemberList