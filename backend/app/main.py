# Entire backend starts here.
# This is the main backend application entrypoint and Creates a FastAPI App


# Responsibilities:
#     initialize FastAPI
#     define routes 
#     define health checks
#     Connects transaction routes to FastAPI app, without this routes will never be available


from fastapi import FastAPI
import redis
from sqlalchemy import text
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler


# Import Transaction, Metrics, User API Routes
from backend.api.transaction_routes import router as transaction_router
from backend.api.metrics_routes import (router as metrics_router)
from backend.api.user_routes import (router as user_router)     # Adds user API endpoints to FastAPI app.


from backend.core.database import engine
from backend.core.request_middleware import (log_requests)
from backend.core.config import (settings)
from backend.core.rate_limiter import (limiter)     #Imports a rate limiter to limit incoming requests from client ip addresses


app = FastAPI(
    title="PulsePay",
    version="1.0.0"
)

#adding limiter to limit the number of incoming requests
app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.middleware("http")(log_requests)    # Register Middleware In FastAPI. Activates request tracing middleware.

app.include_router(transaction_router)  # Makes transaction API endpoints accessible in the FASTAPI app.
app.include_router(metrics_router)      # Makes metrics API endpoints accessible in the FASTAPI app.
app.include_router(user_router)         # Adds user API endpoints to FastAPI in the FASTAPI app.


@app.get("/")
def root():
    return {
        "message": "PulsePay API Running"
    }


# Health: Is the application alive?
@app.get("/health")
def health_check():

    db_status = "healthy"
    redis_status = "healthy"

    try:

        with engine.connect() as connection:

            connection.execute(
                text("SELECT 1")
            )

    except Exception:

        db_status = "unhealthy"

    try:

        redis_client = redis.from_url(
            settings.REDIS_URL
        )

        redis_client.ping()

    except Exception:

        redis_status = "unhealthy"

    overall_status = (
        "healthy"
        if (
            db_status == "healthy"
            and
            redis_status == "healthy"
        )
        else
        "unhealthy"
    )

    return {
        "status": overall_status,
        "database": db_status,
        "redis": redis_status
    }



#Readiness: Can the application serve traffic?
@app.get("/ready")
def readiness_check():

    try:

        with engine.connect() as connection:

            connection.execute(
                text("SELECT 1")
            )

        return {
            "status": "ready"
        }

    except Exception:

        return {
            "status": "not_ready"
        }

# What Swagger Does: Automatically generates API documentation/testing UI.
# Very useful for backend development.