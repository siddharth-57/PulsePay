# Create Request ID Middleware
# What This Step Does: Adds unique request tracing IDs. Every API request now gets: request_id
# This is VERY important in distributed systems.

# It allows tracing:
#     logs
#     retries
#     failures
#     across services.

import time
import uuid

from fastapi import Request

from backend.core.logger import logger


async def log_requests(
    request: Request,
    call_next
):

    request_id = str(uuid.uuid4())

    start_time = time.time()

    logger.info(
        f"Request started | "
        f"request_id={request_id} | "
        f"path={request.url.path}"
    )

    response = await call_next(request)

    process_time = (
        time.time() - start_time
    )

    logger.info(
        f"Request completed | "
        f"request_id={request_id} | "
        f"status_code={response.status_code} | "
        f"duration={process_time:.4f}s"
    )

    response.headers[
        "X-Request-ID"
    ] = request_id

    return response

# WHAT THIS NOW ADDS:
# Every request now logs:
#     Field	Purpose
#     request_id	Trace request lifecycle
#     path	API endpoint
#     duration	API execution time
#     status_code	Response result

# This is REAL observability engineering.