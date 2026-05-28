# Service layer contains:
    # business logic
    # transaction rules
    # orchestration logic

# This keeps API routes thin and clean.

# Professional systems separate:
    # API layer
    # service layer
    # repository layer

from sqlalchemy.orm import Session

from backend.repositories.transaction_repository import (
    TransactionRepository
)

from backend.services.payment_processor import (
    PaymentProcessor
)

#What This Step Does:
# Replaces simplistic idempotency with production-style protection.
# Now: same request → same response but same key + different payload → rejected
# This is REAL payment API behavior.

from backend.services.idempotency_service import (
    IdempotencyService
)                                                   

class TransactionService:

    @staticmethod
    def create_transaction(
        db: Session,
        amount,
        currency,
        idempotency_key
    ):

        payload = {
            "amount": float(amount),
            "currency": currency
        }

        existing_transaction = (
            IdempotencyService.validate_idempotency(
                db=db,
                idempotency_key=idempotency_key,
                payload=payload
            )
        )

        if existing_transaction:
            return existing_transaction

        transaction = (
            TransactionRepository.create_transaction(
                db=db,
                amount=amount,
                currency=currency,
                idempotency_key=idempotency_key
            )
        )

        IdempotencyService.store_idempotency_key(
            db=db,
            idempotency_key=idempotency_key,
            payload=payload,
            transaction_id=transaction.id
        )

    #Adds async processing trigger after transaction creation.Now every payment automatically enters async processing flow.
        PaymentProcessor.process_payment(
            transaction.id
        )

        return transaction