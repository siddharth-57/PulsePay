# What This Step Does: Creates lightweight Transaction metrics collector.

# Tracks:
#     total transactions
#     successes
#     failures

# This introduces: operational metrics

from sqlalchemy.orm import Session

from backend.models.system_metrics import (
    SystemMetrics
)


class MetricsService:

    @staticmethod
    def increment_metric(
        db: Session,
        metric_name: str
    ):

        metric = (
            db.query(SystemMetrics)
            .filter(
                SystemMetrics.metric_name
                == metric_name
            )
            .first()
        )

        if not metric:

            metric = SystemMetrics(
                metric_name=metric_name,
                metric_value=0
            )

            db.add(metric)

        metric.metric_value += 1

        db.commit()

    @staticmethod
    def get_metrics(
        db: Session
    ):

        metrics = (
            db.query(SystemMetrics)
            .all()
        )

        return {
            metric.metric_name:
            metric.metric_value

            for metric in metrics
        }