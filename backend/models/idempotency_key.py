# Create Idempotency Event Model
# What This Step Does

# Creates dedicated table for tracking:
#     request fingerprints
#     request state
#     cached responses

# This separates:
# payment records from request tracking

import uuid

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.sql import func

from backend.core.database import Base


class IdempotencyKey(Base):

    __tablename__ = "idempotency_keys"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    idempotency_key = Column(
        String,
        unique=True,
        nullable=False
    )

    request_hash = Column(
        String,
        nullable=False
    )

    response_transaction_id = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )