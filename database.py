from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel, Session, create_engine


class Link(SQLModel, table=True):
    __tablename__ = "links"

    id: Optional[int] = Field(default=None, primary_key=True)
    original_url: str
    short_name: str = Field(index=True, unique=True)
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime, server_default=func.now()),
    )


engine = None


def init_db(database_url: str):
    global engine
    engine = create_engine(database_url)
    SQLModel.metadata.create_all(engine)
    return engine


def get_session():
    return Session(engine)
