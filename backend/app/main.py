# This is the main backend application entrypoint and Creates FastAPI App

# Responsibilities:
#     initialize FastAPI
#     define routes 
#     define health checks
#     Connects transaction routes to FastAPI app, without this routes will never be available

# Entire backend starts here.

from fastapi import FastAPI
from sqlalchemy import text

from backend.api.transaction_routes import router as transaction_router

from backend.core.database import engine

from backend.core.request_middleware import (
    log_requests
)

from backend.api.metrics_routes import (
    router as metrics_router
)

app = FastAPI(
    title="PulsePay",
    version="1.0.0"
)

app.middleware("http")(log_requests)    #Register Middleware In FastAPI. Activates request tracing middleware.

app.include_router(transaction_router)

app.include_router(metrics_router)  #Makes metrics endpoint accessible.

@app.get("/")
def root():

    return {
        "message": "PulsePay API Running"
    }


@app.get("/health")
def health_check():

    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "healthy"
    }

# What Swagger Does: Automatically generates API documentation/testing UI.
# Very useful for backend development.