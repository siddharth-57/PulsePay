# Create Authentication Dependency
# creates a FastAPI authentication middleware/dependency that extracts the JWT token from the request, validates it, 
# fetches the corresponding user from PostgreSQL, and makes that authenticated user available to protected endpoints.

from fastapi import (
    Depends,
    HTTPException
)

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from sqlalchemy.orm import Session

from backend.core.database import (
    get_db
)

from backend.core.security import (
    verify_access_token
)

from backend.repositories.user_repository import (
    UserRepository
)

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
    db: Session = Depends(
        get_db
    )
):

    token = credentials.credentials

    payload = verify_access_token(
        token
    )

    if not payload:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = (
        UserRepository.get_by_id(
            db,
            payload["sub"]
        )
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user