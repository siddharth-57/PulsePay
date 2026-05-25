# Create Audit Logging Service

# What This Step Does:
#     Tracks ALL transaction state changes.

# Financial systems REQUIRE:
#     traceability
#     audit history
#     observability

# This is critical infrastructure engineering.

from sqlalchemy.orm import Session

from backend.models.audit_log import AuditLog


class AuditService:

    @staticmethod
    def create_log(
        db: Session,
        transaction_id: str,
        old_status: str,
        new_status: str
    ):

        log = AuditLog(
            transaction_id=transaction_id,
            old_status=old_status,
            new_status=new_status
        )

        db.add(log)

        db.commit()

# WHAT THIS SERVICE DOES

# Every time transaction status changes:
# CREATED → PROCESSING
# PROCESSING → SUCCESS

# we store history permanently.