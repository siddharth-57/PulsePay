# JWT Authentication Service Setup
# What This Step Does:
#     Login Endpoint
#     JWT Token Creation
#     JWT Validation
#     Protected APIs


from backend.repositories.user_repository import (
    UserRepository
)

from backend.core.security import (
    verify_password,
    create_access_token
)


class AuthService:

    @staticmethod
    def login(
        db,
        email,
        password
    ):

        user = (
            UserRepository.get_by_email(
                db,
                email
            )
        )

        if not user:

            return None

        if not verify_password(
            password,
            user.password_hash
        ):

            return None

        token = create_access_token(
            user.id
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }