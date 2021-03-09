from uuid import uuid4
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Model(Base):
    __tablename__ = 'users'
    __name__ = 'users'

    id = Column(
        String(uuid4()),
        primary_key=True,
        default=uuid4
    )
    username = Column(
        String,
        unique=True
    )
    password = Column(String)
    email = Column(
        String,
        unique=True
    )
    enabled = Column(
        String,
        default=False
    )
