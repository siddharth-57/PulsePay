# Create FastAPI Test Client
# Creates reusable API testing client.
# Instead of making every test perform login and JWT generation, 
# we'll override authentication in the test environment.

import tests.test_config    #Every pytest run Uses test database

from fastapi.testclient import TestClient

from backend.app.main import app

from backend.core.auth import (
    get_current_user
)


class MockUser:

    id = "test-user"

    email = "test@pulsepay.com"

    role = "admin"                      #admin-only metrics endpoint will be allowed.


def override_get_current_user():

    return MockUser()               #mock user is returned so login won't be needed


app.dependency_overrides[
    get_current_user
] = override_get_current_user

client = TestClient(app)