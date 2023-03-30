from __future__ import annotations

from pydantic import BaseModel


class ParticipantCreateRequest(BaseModel):
    name: str
    wish: str | None

    class Config:
        orm_mode = True


class ParticipantBaseScheme(BaseModel):
    id: int
    name: str
    wish: str | None

    class Config:
        orm_mode = True


class ParticipantScheme(ParticipantBaseScheme):
    recipient: ParticipantBaseScheme | None

    class Config:
        orm_mode = True
