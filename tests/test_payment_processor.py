# What This File Does
# Tests the core payment simulation engine independently from Celery.

from backend.services.payment_processor import (
    PaymentProcessor
)


def test_payment_processor_exists():

    assert PaymentProcessor


def test_payment_processor_has_method():

    assert hasattr(
        PaymentProcessor,
        "process_payment"
    )