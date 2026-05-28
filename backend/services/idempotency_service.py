# What This Step Does

# Centralizes:
#     duplicate request detection
#     request validation
#     safe response handling

# This becomes the core payment protection layer.

from fastapi import HTTPException

from sqlalchemy.orm import Session

from backend.core.hash_utils import (
    generate_request_hash
)

from backend.repositories.idempotency_repository import (
    IdempotencyRepository
)

from backend.repositories.transaction_repository import (
    TransactionRepository
)


class IdempotencyService:

    @staticmethod
    def validate_idempotency(
        db: Session,
        idempotency_key: str,
        payload: dict
    ):

        request_hash = (
            generate_request_hash(payload)
        )

        existing_key = (
            IdempotencyRepository.get_by_key(
                db,
                idempotency_key
            )
        )

        if existing_key:

            if (
                existing_key.request_hash
                != request_hash
            ):

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Idempotency key reused "
                        "with different payload"
                    )
                )

            transaction = (
                TransactionRepository
                .get_transaction_by_id(
                    db,
                    existing_key.response_transaction_id
                )
            )

            return transaction

        return None

    @staticmethod
    def store_idempotency_key(
        db: Session,
        idempotency_key: str,
        payload: dict,
        transaction_id: str
    ):

        request_hash = (
            generate_request_hash(payload)
        )

        return (
            IdempotencyRepository.create_key(
                db=db,
                idempotency_key=idempotency_key,
                request_hash=request_hash,
                response_transaction_id=transaction_id
            )
        )