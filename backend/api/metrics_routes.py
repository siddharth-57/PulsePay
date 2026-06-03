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

from backend.core.auth import (
    get_current_user
)

from backend.core.authorization import (
    require_admin
)

router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"]
)

#Only returns metrics to users with a valid token
@router.get("/")
def get_metrics(
    db: Session = Depends(get_db),
    current_user = Depends(
        get_current_user
    )
):

    require_admin(                      #metrics endpoint is available to admin only
        current_user
    )

    return MetricsService.get_metrics(db)