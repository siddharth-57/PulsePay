# Role-Based Authorization
# Authenticated User -> Role Checked -> Allow / Deny
# This file checks if the given user is an admin or not

from fastapi import (HTTPException)


def require_admin(
    current_user
):

    if current_user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user