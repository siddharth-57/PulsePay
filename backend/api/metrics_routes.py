# What This Step Does: Exposes transaction metrics through API.

# Operations teams can now monitor:
#     throughput
#     success rate
#     failures

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from backend.core.dependencies import (
    get_db
)

from backend.services.metrics_service import (
    MetricsService
)

router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"]
)


@router.get("/")
def get_metrics(
    db: Session = Depends(get_db)
):

    return MetricsService.get_metrics(db)