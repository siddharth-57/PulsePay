# What This Step Does
# Creates simulated:
#     Dead Letter Queue system
#     Dead Letter Queue (DLQ) stores permanently failed jobs.

# Real systems use DLQs for:
#     manual investigation
#     operational debugging
#     replaying failed events

class DeadLetterService:

    @staticmethod
    def send_to_dead_letter_queue(
        transaction_id: str
    ):

        print(
            f"[DEAD LETTER QUEUE] "
            f"Transaction {transaction_id} "
            f"moved to dead letter queue"
        )

# A dead-letter queue means: "This task failed too many times."

# So instead of retrying forever:
#     system isolates it
#     operators can investigate later

# This is a CORE distributed systems pattern.
