# What This Step Does
# Handles:
#     idempotency lookups
#     duplicate detection
#     response caching
# Repository pattern keeps DB logic isolated.

# Repository means: A dedicated layer/class responsible for all database operations related to a specific entity or feature
# Without repository pattern, database queries get scattered everywhere.

from sqlalchemy.orm import Session

from backend.models.idempotency_key import (
    IdempotencyKey
)


class IdempotencyRepository:

    @staticmethod
    def get_by_key(
        db: Session,
        idempotency_key: str
    ):

        return (
            db.query(IdempotencyKey)
            .filter(
                IdempotencyKey.idempotency_key
                == idempotency_key
            )
            .first()
        )

    @staticmethod
    def create_key(
        db: Session,
        idempotency_key: str,
        request_hash: str,
        response_transaction_id: str
    ):

        record = IdempotencyKey(
            idempotency_key=idempotency_key,
            request_hash=request_hash,
            response_transaction_id=response_transaction_id
        )

        db.add(record)

        db.commit()

        db.refresh(record)

        return record