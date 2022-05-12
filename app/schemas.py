from pydantic import BaseModel


class MeetingBase(BaseModel):
    type: str
    date: str
    time: str
    link: str


class CreateMeeting(MeetingBase):
    pass


class Meeting(MeetingBase):
    id: int

    class Config:
        orm_mode = True


class MemberBase(BaseModel):
    name: str


class CreateMember(MemberBase):
    pass


class Member(MemberBase):
    id: int
    msg: str | None = None

    class Config:
        orm_mode = True


class LegislationBase(BaseModel):
    record_num: str
    type: str
    title: str
    result: str
    action_text: str
    mtg_date: str


class CreateLegislation(LegislationBase):
    pass


class Legislation(LegislationBase):
    id: int

    class Config:
        orm_mode = True


class VoteBase(BaseModel):
    record_num: str
    name: str
    vote: str


class CreateVote(VoteBase):
    pass


class Vote(VoteBase):
    id: int

    class Config:
        orm_mode = True
