# Event Flow

# This file explains:

How events move through the system
Async workflows
Event-driven architecture
This introduces distributed systems concepts.

## Internal Events

- PAYMENT_CREATED
- PAYMENT_PROCESSING
- PAYMENT_SUCCESS
- PAYMENT_FAILED
- REFUND_INITIATED
- REFUND_COMPLETED

---

# Example Event Flow

1. API receives payment request
2. PAYMENT_CREATED event emitted
3. Worker consumes event
4. Payment processing begins
5. PAYMENT_SUCCESS or PAYMENT_FAILED emitted
6. Webhook delivery triggered
7. Notification service triggered