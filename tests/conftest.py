# Create FastAPI Test Client
# Creates reusable API testing client.

import tests.test_config    #Every pytest run Uses test database

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)