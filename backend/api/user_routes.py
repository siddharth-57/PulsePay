# What This Step Does: Creates registration endpoint to registers users.

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from backend.core.database import (
    get_db
)

from backend.schemas.user import (
    UserCreate
)

from backend.services.user_service import (
    UserService
)

from backend.schemas.user import (
    LoginRequest
)

from backend.services.auth_service import (
    AuthService
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# @router.post("/")
from backend.schemas.user import (
    UserCreate,
    UserResponse
)
@router.post(
    "/",
    response_model=UserResponse
)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db)
):

    try:

        return UserService.create_user(
            db,
            payload.email,
            payload.password
        )

    except ValueError as ex:

        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )
    
#Login Endpoint
@router.post("/login")
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db)
):

    result = AuthService.login(
        db,
        payload.email,
        payload.password
    )

    if not result:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    return result