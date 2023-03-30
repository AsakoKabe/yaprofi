from sqlalchemy import Column, TEXT, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from app.db.models import BaseTable


class Participant(BaseTable):
    __tablename__ = "participant"

    name = Column(TEXT)
    wish = Column(TEXT)
    children: "Participant" = relationship(
        "Participant",
        backref=backref('parent', remote_side='Participant.id'),
    )
    parent_id = Column(
        Integer,
        ForeignKey('participant.id', ondelete='CASCADE'),
        nullable=True
        )

    group_id = Column(Integer, ForeignKey("group.id", ondelete="CASCADE"))
    group = relationship("Group", back_populates="participants")
