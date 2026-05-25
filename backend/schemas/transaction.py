# This file is in pydantic schemas folder.
# Pydantic schemas define:
#     API request structures
#     API response structures
#     validation rules

# This separates:
#     database models from API contracts
#     Very important backend architecture principle.


# This file Defines:
#     payment creation request
#     payment response
#     validation rules
# FastAPI automatically validates incoming requests using these schemas.

from decimal import Decimal

from pydantic import BaseModel

from backend.models.transaction_status import TransactionStatus


class CreateTransactionRequest(BaseModel):

    amount: Decimal

    currency: str


class TransactionResponse(BaseModel):

    id: str

    amount: Decimal

    currency: str

    status: TransactionStatus

    retry_count: int   #Exposes retry information in APIs.Clients/operators can now see: how many retries occurred. This improves observability.

    class Config:

        from_attributes = True