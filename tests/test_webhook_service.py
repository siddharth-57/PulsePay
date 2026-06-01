# What This File Does
# Verifies:
#     WebhookService exists
#     create_webhook_event method exists

from backend.services.webhook_service import (
    WebhookService
)


def test_webhook_service_exists():

    assert WebhookService


def test_webhook_service_has_method():

    assert hasattr(
        WebhookService,
        "create_webhook_event"
    )