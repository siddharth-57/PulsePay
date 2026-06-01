# What This File Does: Tests that duplicate requests do not create duplicate transactions.
#same request + same idempotency key = same transaction

from tests.conftest import client

def test_same_request_returns_same_transaction():

    payload = {
        "amount": 500,
        "currency": "USD"
    }

    headers = {
        "idempotency-key": "duplicate-test"
    }

    response_1 = client.post(
        "/transactions/",
        headers=headers,
        json=payload
    )

    response_2 = client.post(
        "/transactions/",
        headers=headers,
        json=payload
    )

    assert (
        response_1.json()["id"]
        ==
        response_2.json()["id"]
    )


# Verifies: same key + different payload = request rejected
def test_same_key_different_payload():

    headers = {
        "idempotency-key": "invalid-key"
    }

    client.post(
        "/transactions/",
        headers=headers,
        json={
            "amount": 100,
            "currency": "USD"
        }
    )

    response = client.post(
        "/transactions/",
        headers=headers,
        json={
            "amount": 999,
            "currency": "USD"
        }
    )

    assert response.status_code == 400