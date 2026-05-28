from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from backend.core.database import Base


class SystemMetrics(Base):

    __tablename__ = "system_metrics"

    metric_name = Column(
        String,
        primary_key=True
    )

    metric_value = Column(
        Integer,
        default=0
    )