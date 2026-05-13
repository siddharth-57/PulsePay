# This is the main backend application entrypoint and Creates FastAPI App

# Responsibilities:
#     initialize FastAPI
#     define routes
#     define health checks

# Entire backend starts here.

from fastapi import FastAPI
from sqlalchemy import text

from backend.core.database import engine


app = FastAPI(
    title="PulsePay",
    version="1.0.0"
)


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