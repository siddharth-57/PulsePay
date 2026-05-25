# Repository layer handles:
#     database queries
#     inserts
#     updates

# This keeps database logic OUT of API routes.
# This is professional backend architecture.

from sqlalchemy.orm import Session

from backend.models.transaction import Transaction


class TransactionRepository:

    @staticmethod
    def create_transaction(
        db: Session,
        amount,
        currency,
        idempotency_key
    ):

        transaction = Transaction(
            amount=amount,
            currency=currency,
            idempotency_key=idempotency_key
        )

        db.add(transaction)

        db.commit()

        db.refresh(transaction)

        return transaction

    @staticmethod
    def get_transaction_by_id(
        db: Session,
        transaction_id: str
    ):

        return (
            db.query(Transaction)
            .filter(Transaction.id == transaction_id)
            .first()
        )

    @staticmethod
    def get_transaction_by_idempotency_key(
        db: Session,
        idempotency_key: str
    ):

        return (
            db.query(Transaction)
            .filter(
                Transaction.idempotency_key == idempotency_key
            )
            .first()
        )