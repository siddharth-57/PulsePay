# What This Step Does:
# Creates database table for storing webhook delivery events.
# This tracks:
#     delivery attempts
#     delivery status
#     retries
#     payload history

# This is critical for reliability.

import uuid

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.sql import func

from backend.core.database import Base


class WebhookEvent(Base):

    __tablename__ = "webhook_events"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    transaction_id = Column(
        String,
        nullable=False
    )

    event_type = Column(
        String,
        nullable=False
    )

    delivery_status = Column(
        String,
        default="PENDING"
    )

    retry_count = Column(
        Integer,
        default=0
    )

    delivered = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )