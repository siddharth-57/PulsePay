# What This Step Does
# Creates service responsible for:
# dispatching background jobs
# communicating with Celery
# This separates:
    # API logic from async infrastructure

from backend.tasks.payment_tasks import (
    process_payment_task
)


class PaymentProcessor:

    @staticmethod
    def process_payment(transaction_id: str):

        process_payment_task.delay(transaction_id)