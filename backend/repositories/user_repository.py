# Create User Repository
# What This Step Does: Database access layer for users.
# Purpose: Handles user queries and persistence.

from sqlalchemy.orm import Session

from backend.models.user import User


class UserRepository:

    @staticmethod
    def create_user(
        db: Session,
        user: User
    ):

        db.add(user)

        db.commit()

        db.refresh(user)

        return user

    @staticmethod
    def get_by_email(
        db: Session,
        email: str
    ):

        return (
            db.query(User)
            .filter(
                User.email == email
            )
            .first()
        )
    
# Add User Lookup Repository Method
    @staticmethod
    def get_by_id(
        db: Session,
        user_id: str
    ):

        return (
            db.query(User)
            .filter(
                User.id == user_id
            )
            .first()
        )