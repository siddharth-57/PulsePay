# What This Step Does: Creates users and hashes passwords.

import uuid

from backend.models.user import User

from backend.core.security import (
    hash_password
)

from backend.repositories.user_repository import (
    UserRepository
)


class UserService:

    @staticmethod
    def create_user(
        db,
        email,
        password
    ):

        existing_user = (
            UserRepository.get_by_email(
                db,
                email
            )
        )

        if existing_user:

            raise ValueError(
                "User already exists"
            )

        user = User(
            id=str(uuid.uuid4()),
            email=email,
            password_hash=hash_password(
                password
            )
        )

        return (
            UserRepository.create_user(
                db,
                user
            )
        )