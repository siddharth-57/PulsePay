# What This Step Does: Generates request fingerprint hashes.

# This ensures:
# same idempotency key with DIFFERENT request body is rejected.
# same request will always generate same hash 

# Very important fintech safety feature.


import hashlib
import json


def generate_request_hash(
    payload: dict
):

    payload_string = json.dumps(
        payload,
        sort_keys=True
    )

    return hashlib.sha256(
        payload_string.encode()
    ).hexdigest()

