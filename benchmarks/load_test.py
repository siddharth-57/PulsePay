import os
import statistics
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed

import httpx
from dotenv import load_dotenv


load_dotenv("benchmarks/.env")


BASE_URL = "http://localhost:8000"

USERNAME = os.environ["PULSEPAY_USERNAME"]
PASSWORD = os.environ["PULSEPAY_PASSWORD"]


# Capacity test:
# 5,000 requests at different concurrency levels
CAPACITY_TESTS = [
    (5000, 50),
    (5000, 100),
    (5000, 200),
]

# Sustained load test:
SUSTAINED_REQUESTS = 50000
SUSTAINED_WORKERS = 100


def login() -> str:

    response = httpx.post(
        f"{BASE_URL}/users/login",
        json={
            "email": USERNAME,
            "password": PASSWORD,
        },
    )

    response.raise_for_status()

    return response.json()["access_token"]


def percentile(values, percentile_value):

    values = sorted(values)

    index = int(
        (percentile_value / 100)
        * (len(values) - 1)
    )

    return values[index]


def send_transaction(token: str):

    start = time.perf_counter()

    transaction_id = None

    try:
        response = httpx.post(
            f"{BASE_URL}/transactions/",
            json={
                "amount": 100,
                "currency": "USD",
            },
            headers={
                "Authorization": f"Bearer {token}",
                "idempotency-key": str(uuid.uuid4()),
            },
            timeout=30.0,
        )

        latency = (
            time.perf_counter() - start
        ) * 1000

        if response.is_success:
            transaction_id = response.json()["id"]

        return response, latency, transaction_id

    except httpx.RequestError:

        latency = (
            time.perf_counter() - start
        ) * 1000

        return None, latency, None


def run_load_test(
    token,
    total_requests,
    concurrent_workers,
    test_name,
):

    latencies = []

    successful_requests = 0
    failed_requests = 0

    transaction_ids = []

    start = time.perf_counter()

    with ThreadPoolExecutor(
        max_workers=concurrent_workers
    ) as executor:

        futures = [
            executor.submit(
                send_transaction,
                token,
            )
            for _ in range(total_requests)
        ]

        for future in as_completed(futures):

            response, latency, transaction_id = (
                future.result()
            )

            latencies.append(latency)

            if response is not None and response.is_success:
            
                successful_requests += 1
            
                if transaction_id:
                    transaction_ids.append(
                        transaction_id
                    )
            
            else:
            
                failed_requests += 1

    duration = time.perf_counter() - start

    throughput = (
        total_requests / duration
    )

    error_rate = (
        failed_requests / total_requests
    ) * 100

    p95_latency = percentile(
        latencies,
        95,
    )

    print()
    print(
        f"========== {test_name} =========="
    )

    print(
        f"Total requests: {total_requests}"
    )

    print(
        f"Concurrent workers: {concurrent_workers}"
    )

    print(
        f"Successful requests: "
        f"{successful_requests}"
    )

    print(
        f"Failed requests: "
        f"{failed_requests}"
    )

    print(
        f"Duration: "
        f"{duration:.2f} seconds"
    )

    print(
        f"Throughput: "
        f"{throughput:.2f} requests/sec"
    )

    print(
        f"Error rate: "
        f"{error_rate:.2f}%"
    )

    print(
        f"P95 latency: "
        f"{p95_latency:.2f} ms"
    )

    print(
        "============================================"
    )

    return transaction_ids


def main():

    token = login()

    print()
    print("Starting PulsePay load tests...")
    print()

    # Capacity sweep
    for total_requests, workers in CAPACITY_TESTS:

        run_load_test(
            token=token,
            total_requests=total_requests,
            concurrent_workers=workers,
            test_name=(
                f"CAPACITY TEST - "
                f"{workers} workers"
            ),
        )

    # Sustained load test
    run_load_test(
        token=token,
        total_requests=SUSTAINED_REQUESTS,
        concurrent_workers=SUSTAINED_WORKERS,
        test_name=(
            "SUSTAINED LOAD TEST - "
            "50,000 requests / 100 workers"
        ),
    )


if __name__ == "__main__":
    main()