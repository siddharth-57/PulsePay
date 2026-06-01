# Create Transaction API Tests
# What This Step Does
# Tests:
#     transaction creation
#     response structure

from tests.conftest import client


def test_create_transaction():

    response = client.post(
        "/transactions/",
        headers={
            "idempotency-key":
            "test-transaction-1"
        },
        json={
            "amount": 100,
            "currency": "USD"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert float(data["amount"]) == 100.00

    assert data["currency"] == "USD"