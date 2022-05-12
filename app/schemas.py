from re import S
from pydantic import BaseModel


class MeetingBase(BaseModel):
    type: str
    date: str
    time: str
    link: str


class CreateMeeting(MeetingBase):
    pass


class MemberBase(BaseModel):
    name: str


class CreateMember(MemberBase):
    pass


class LegislationBase(BaseModel):
    record_num: str
    type: str
    title: str
    result: str
    action_text: str
    mtg_date: str


class CreateLegislation(LegislationBase):
    pass


class VoteBase(BaseModel):
    record_num: str
    name: str
    vote: str


class CreateVote(VoteBase):
    pass
