from sqlalchemy import INTEGER, Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db import DeclarativeBase


class BaseTable(DeclarativeBase):
    __abstract__ = True

    # id = Column(
    #     UUID(as_uuid=True),
    #     primary_key=True,
    #     server_default=func.gen_random_uuid(),
    #     unique=True,
    #     doc="Unique index of element (type UUID)",
    # )
    id = Column(
        INTEGER,
        primary_key=True,
        autoincrement=True,
        unique=True,
        doc="Unique index of element (type int)",
    )

    def __repr__(self):
        columns = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return f'<{self.__tablename__}: {", ".join(map(lambda x: f"{x[0]}={x[1]}", columns.items()))}>'
