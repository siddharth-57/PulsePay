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

REQUEST_COUNTS = [100, 500, 1000, 5000]
CONCURRENT_WORKERS = 50

TRANSACTION_POLL_INTERVAL = 1


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
    )

    latency = (time.perf_counter() - start) * 1000

    if response.is_success:
        transaction_id = response.json()["id"]

    return response, latency, transaction_id


def print_api_results(
    test_type,
    total_requests,
    latencies,
    successful_requests,
    failed_requests,
    total_time,
):
    print()
    print(f"========== {test_type} API PERFORMANCE ==========")
    print(f"Total API requests: {total_requests}")
    print(f"API requests successful: {successful_requests}")
    print(f"API requests failed: {failed_requests}")

    print(
        f"API Request Success Rate: "
        f"{(successful_requests / total_requests) * 100:.2f}%"
    )

    print(
        f"API Request Failure Rate: "
        f"{(failed_requests / total_requests) * 100:.2f}%"
    )

    print(
        f"API Request Average Latency: "
        f"{statistics.mean(latencies):.2f} ms"
    )

    print(
        f"API Request P50 Latency: "
        f"{percentile(latencies, 50):.2f} ms"
    )

    print(
        f"API Request P95 Latency: "
        f"{percentile(latencies, 95):.2f} ms"
    )

    print(
        f"API Request P99 Latency: "
        f"{percentile(latencies, 99):.2f} ms"
    )

    print(
        f"API Request Throughput: "
        f"{total_requests / total_time:.2f} requests/sec"
    )

    print("============================================")


def get_transaction_status(transaction_id):
    response = httpx.get(
        f"{BASE_URL}/transactions/{transaction_id}"
    )

    if not response.is_success:
        return None

    return response.json()["status"]


def collect_transaction_results(transaction_ids):
    successful_transactions = 0
    failed_transactions = 0

    remaining_ids = set(transaction_ids)

    processing_start = time.perf_counter()

    print()
    print("Waiting for payment transactions to complete...")

    while remaining_ids:

        completed_ids = set()

        for transaction_id in remaining_ids:

            status = get_transaction_status(transaction_id)

            if status == "SUCCESS":
                successful_transactions += 1
                completed_ids.add(transaction_id)

            elif status == "FAILED":
                failed_transactions += 1
                completed_ids.add(transaction_id)

        remaining_ids -= completed_ids

        completed_count = (
            successful_transactions
            + failed_transactions
        )

        print(
            f"\rTransactions completed: "
            f"{completed_count}/{len(transaction_ids)}",
            end="",
            flush=True,
        )

        if remaining_ids:
            time.sleep(TRANSACTION_POLL_INTERVAL)

    processing_time = (
        time.perf_counter()
        - processing_start
    )

    total_transactions = len(transaction_ids)

    print()
    print()
    print(
        "========== PAYMENT TRANSACTION RESULTS =========="
    )

    print(
        f"Total transactions created: "
        f"{total_transactions}"
    )

    print(
        f"Successful transactions: "
        f"{successful_transactions}"
    )

    print(
        f"Failed transactions: "
        f"{failed_transactions}"
    )

    print(
        "Pending transactions: 0"
    )

    print(
        f"Transaction Success Rate: "
        f"{(successful_transactions / total_transactions) * 100:.2f}%"
    )

    print(
        f"Transaction Failure Rate: "
        f"{(failed_transactions / total_transactions) * 100:.2f}%"
    )

    print(
        f"Total payment processing time: "
        f"{processing_time:.2f} seconds"
    )

    print(
        "=================================================")


def run_sequential(token, total_requests):
    latencies = []
    successful_requests = 0
    failed_requests = 0
    transaction_ids = []

    total_start = time.perf_counter()

    for _ in range(total_requests):

        response, latency, transaction_id = send_transaction(
            token
        )

        latencies.append(latency)

        if response.is_success:
            successful_requests += 1

            if transaction_id:
                transaction_ids.append(transaction_id)

        else:
            failed_requests += 1

    total_time = time.perf_counter() - total_start

    print_api_results(
        "SEQUENTIAL",
        total_requests,
        latencies,
        successful_requests,
        failed_requests,
        total_time,
    )

    collect_transaction_results(
        transaction_ids
    )


def run_concurrent(token, total_requests):
    latencies = []
    successful_requests = 0
    failed_requests = 0
    transaction_ids = []

    total_start = time.perf_counter()

    with ThreadPoolExecutor(
        max_workers=CONCURRENT_WORKERS
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

            if response.is_success:
                successful_requests += 1

                if transaction_id:
                    transaction_ids.append(
                        transaction_id
                    )

            else:
                failed_requests += 1

    total_time = time.perf_counter() - total_start

    print_api_results(
        "CONCURRENT",
        total_requests,
        latencies,
        successful_requests,
        failed_requests,
        total_time,
    )

    collect_transaction_results(
        transaction_ids
    )


def main():
    token = login()

    for total_requests in REQUEST_COUNTS:

        print()
        print(
            f"Running sequential test: "
            f"{total_requests} requests"
        )

        run_sequential(
            token,
            total_requests,
        )

        print()
        print(
            f"Running concurrent test: "
            f"{total_requests} requests"
        )

        run_concurrent(
            token,
            total_requests,
        )


if __name__ == "__main__":
    main()