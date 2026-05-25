# Defines payment-related API endpoints.
# This is the public interface of the backend.

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException

from sqlalchemy.orm import Session

from backend.core.dependencies import get_db

from backend.repositories.transaction_repository import (
    TransactionRepository
)

from backend.schemas.transaction import (
    CreateTransactionRequest,
    TransactionResponse
)

from backend.services.transaction_service import (
    TransactionService
)

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


@router.post(
    "/",
    response_model=TransactionResponse
)
def create_transaction(
    request: CreateTransactionRequest,
    db: Session = Depends(get_db),
    idempotency_key: str = Header(...)
):

    transaction = (
        TransactionService.create_transaction(
            db=db,
            amount=request.amount,
            currency=request.currency,
            idempotency_key=idempotency_key
        )
    )

    return transaction


@router.get(
    "/{transaction_id}",
    response_model=TransactionResponse
)
def get_transaction(
    transaction_id: str,
    db: Session = Depends(get_db)
):

    transaction = (
        TransactionRepository.get_transaction_by_id(
            db,
            transaction_id
        )
    )

    if not transaction:

        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return transaction