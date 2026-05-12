# Database Design

# This file defines:
    Database tables
    Important columns
    System data model
    
    This helps plan backend architecture before coding.

## transactions

| Column | Type |
|---|---|
| id | UUID |
| amount | DECIMAL |
| currency | VARCHAR |
| status | VARCHAR |
| idempotency_key | VARCHAR |
| created_at | TIMESTAMP |
| updated_at | TIMESTAMP |
| retry_count | INTEGER |

---

# audit_logs

| Column | Type |
|---|---|
| id | UUID |
| transaction_id | UUID |
| old_status | VARCHAR |
| new_status | VARCHAR |
| created_at | TIMESTAMP |