# Defines async background payment tasks.
# These tasks simulate:
    # payment processing
    # network delays
    # async execution
# This is the beginning of worker-based distributed processing.


# What This Step Does
# Updates PostgreSQL transaction state after worker finishes processing.
# This creates real async state transitions.


# What This Step Does
# Automatically logs all transaction state transitions.
# Now every payment change becomes traceable.





import random
import time

from backend.core.config import settings

from backend.core.database import SessionLocal

from backend.models.transaction import Transaction

from backend.models.transaction_status import (
    TransactionStatus
)

from backend.core.celery_app import celery_app

from backend.services.audit_service import (
    AuditService
)

from backend.services.dead_letter_service import (
    DeadLetterService
)


@celery_app.task(
    bind=True,
    max_retries=settings.MAX_PAYMENT_RETRIES
)
def process_payment_task(
    self,
    transaction_id: str
):

    db = SessionLocal()

    try:

        transaction = (
            db.query(Transaction)
            .filter(Transaction.id == transaction_id)
            .first()
        )

        if not transaction:
            return

        old_status = transaction.status

        transaction.status = (
            TransactionStatus.PROCESSING
        )

        db.commit()

        AuditService.create_log(
            db=db,
            transaction_id=transaction.id,
            old_status=old_status,
            new_status=TransactionStatus.PROCESSING
        )

        print(
            f"Processing transaction "
            f"{transaction_id}"
        )

        time.sleep(5)

        payment_success = random.choice(
            [
                True,
                False
            ]
        )


#What This Step Does, Adds: automatic retries and audit retries, retry counters, retry delays, dead-letter queue fallback
        
        if not payment_success:     

            transaction.retry_count += 1

            db.commit()

            print(
                f"Transaction {transaction_id} "
                f"failed. Retry count: "
                f"{transaction.retry_count}"
            )

            if (
                transaction.retry_count
                >= settings.MAX_PAYMENT_RETRIES
            ):

                old_status = transaction.status

                transaction.status = (
                    TransactionStatus.FAILED
                )

                db.commit()

                AuditService.create_log(
                    db=db,
                    transaction_id=transaction.id,
                    old_status=old_status,
                    new_status=TransactionStatus.FAILED
                )

                DeadLetterService.send_to_dead_letter_queue(
                    transaction.id
                )

                return

            raise self.retry(
                countdown=settings.PAYMENT_RETRY_DELAY
            )

        old_status = transaction.status

        transaction.status = (
            TransactionStatus.SUCCESS
        )

        db.commit()

        AuditService.create_log(
            db=db,
            transaction_id=transaction.id,
            old_status=old_status,
            new_status=TransactionStatus.SUCCESS
        )

        print(
            f"Transaction {transaction_id} "
            f"completed successfully"
        )

    finally:

        db.close()
        

# WHAT THIS NOW ADDS

# Every transaction now generates:

# PROCESSING audit log
# SUCCESS/FAILED audit log

# This creates a real payment event history system.