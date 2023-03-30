from sqlalchemy import Column, TEXT
from sqlalchemy.orm import relationship

from app.db.models import BaseTable


class Group(BaseTable):
    __tablename__ = "group"

    name = Column(TEXT)
    description = Column(TEXT)
    participants = relationship(
        "Participant", back_populates="group",
        lazy="selectin", passive_deletes=True
    )
