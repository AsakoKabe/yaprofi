from __future__ import annotations

from pydantic import BaseModel

from app.schemas import ParticipantScheme


class GroupCreateRequest(BaseModel):
    name: str
    description: str | None

    class Config:
        orm_mode = True


class GroupBaseScheme(BaseModel):
    id: int
    name: str
    description: str | None

    class Config:
        orm_mode = True


class GroupScheme(GroupBaseScheme):
    participants: list[ParticipantScheme]

    class Config:
        orm_mode = True
