# What This Step Does
# Adds and creates table/model: User Accounts for authentication which stores platform users.

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import DateTime

from datetime import datetime

from backend.core.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        String,
        primary_key=True
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    password_hash = Column(
        String,
        nullable=False
    )

    role = Column(
        String,
        default="user"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
