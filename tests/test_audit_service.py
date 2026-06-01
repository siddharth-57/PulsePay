# What This File Does

# Verifies and tests audit logging services:
#     AuditService exists
#     create_log method exists

from backend.services.audit_service import (
    AuditService
)


def test_audit_service_exists():

    assert AuditService


def test_audit_service_has_method():

    assert hasattr(
        AuditService,
        "create_log"
    )