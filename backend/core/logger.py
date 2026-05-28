#What This Step Does
# Creates centralized logger for:
    # APIs
    # workers
    # services
    # retry flows
# All logs will now follow a standard format.

import logging


logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    )
)

logger = logging.getLogger("pulsepay")

# All logs now become structured like:
# 2026-05-27 12:00:00 | INFO | Payment processing started
# This is MUCH cleaner than random print statements.