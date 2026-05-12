# Transaction Lifecycle

# This file defines:

transaction lifecycle
payment states
refund states
allowed state transitions

## Payment Flow

CREATED
    ↓
PENDING
    ↓
PROCESSING
    ↓
SUCCESS

Failure States:
- FAILED
- TIMEOUT
- CANCELLED

Refund States:
SUCCESS
    ↓
REFUND_PENDING
    ↓
REFUNDED

---

# Transaction State Definitions

## CREATED
Transaction record initialized.

## PENDING
Waiting for worker pickup.

## PROCESSING
Currently being processed by worker.

## SUCCESS
Payment completed successfully.

## FAILED
Payment failed permanently.

## TIMEOUT
Worker exceeded timeout threshold.

## REFUND_PENDING
Refund initiated asynchronously.

## REFUNDED
Refund completed successfully.