# Idempotency Design

# This file explains:
    Duplicate prevention
    Retry-safe APIs
    Idempotency keys

## Goal

Prevent duplicate transaction creation and duplicate payment processing.

---

# Strategy

Clients provide:
- Idempotency-Key header

The backend:
- stores the key
- checks for duplicates
- returns cached response for repeated requests