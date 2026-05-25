# Tracks every transaction state change.

# This is extremely important in payment systems because:
#     payment history must be traceable
#     debugging requires audit trails
#     financial systems require observability

import uuid

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.sql import func

from backend.core.database import Base


class AuditLog(Base):

    __tablename__ = "audit_logs"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    transaction_id = Column(
        String,
        ForeignKey("transactions.id"),
        nullable=False
    )

    old_status = Column(
        String,
        nullable=False
    )

    new_status = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )