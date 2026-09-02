# Loads test environment instead of production environment

# import os

# os.environ["DATABASE_URL"] = (
#     "postgresql://postgres:postgres@localhost:5432/pulsepay_test"
# )

# os.environ["REDIS_URL"] = (
#     "redis://localhost:6379/0"
# )

import os

os.environ["DATABASE_URL"] = (
    "postgresql://postgres:postgres@postgres:5432/pulsepay_test"
)

os.environ["REDIS_URL"] = (
    "redis://redis:6379/0"
)