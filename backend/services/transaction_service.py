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


class TransactionService:

    @staticmethod
    def create_transaction(
        db: Session,
        amount,
        currency,
        idempotency_key
    ):

        existing_transaction = (
            TransactionRepository
            .get_transaction_by_idempotency_key(
                db,
                idempotency_key
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
    #Adds async processing trigger after transaction creation.Now every payment automatically enters async processing flow.
        PaymentProcessor.process_payment(
            transaction.id
        )

        return transaction