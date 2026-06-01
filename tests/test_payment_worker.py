# What This File Does:
# Tests the actual payment worker function.

from backend.tasks.payment_tasks import process_payment_task


def test_payment_worker_executes():

    result = process_payment_task.run(
        "test-transaction-id"
    )

    assert result is None