# What This Step Does

# Defines:
#     Request Validation
#     Response Validation
# for user-related APIs.

# Purpose
# Defines:
#     User Registration Request
#     User Response   

from pydantic import BaseModel


class UserCreate(BaseModel):

    email: str

    password: str


class UserResponse(BaseModel):

    id: str

    email: str

    role: str

# Create Login Schema
class LoginRequest(BaseModel):

    email: str

    password: str