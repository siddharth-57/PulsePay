# Loads test environment instead of production environment

import os

os.environ["DATABASE_URL"] = (
    "postgresql://postgres:postgres@localhost:5432/pulsepay_test"
)