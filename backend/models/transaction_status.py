# Create Transaction Status Enum

# This File:
#     Defines all valid transaction states.

# This prevents:
#     invalid statuses
#     typo bugs
#     inconsistent state management

# Real payment systems are heavily state-machine based.
# Enum means a fixed set of predefined values. It is used when a variable should only contain specific allowed values.
# A transaction status can only be one of these predefined values.


from enum import Enum

class TransactionStatus(str, Enum):

    CREATED = "CREATED"

    PENDING = "PENDING"

    PROCESSING = "PROCESSING"

    SUCCESS = "SUCCESS"

    FAILED = "FAILED"

    TIMEOUT = "TIMEOUT"

    CANCELLED = "CANCELLED"

    REFUND_PENDING = "REFUND_PENDING"

    REFUNDED = "REFUNDED"