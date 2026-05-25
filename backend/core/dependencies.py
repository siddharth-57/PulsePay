# Create Database Session Dependency
# This file creates a reusable database session dependency for FastAPI.
# Every API request that needs database access will use this.

# This is important because:
#     sessions must be properly opened
#     sessions must be properly closed
#     DB connections must not leak

from backend.core.database import SessionLocal


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()