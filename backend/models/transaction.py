# This File Does:
#     Defines the main payments table.It is the source of truth for all payment processing.
#     Every transaction state lives here.

import uuid

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy.sql import func

from backend.core.database import Base
from backend.models.transaction_status import TransactionStatus


class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    currency = Column(
        String,
        nullable=False
    )

    status = Column(
        Enum(TransactionStatus),
        nullable=False,
        default=TransactionStatus.CREATED
    )

    idempotency_key = Column(
        String,
        unique=True,
        nullable=False
    )

    retry_count = Column(
        Integer,
        default=0
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )