# What This Step Does

# Handles webhook DB operations:
#     create webhook events
#     update delivery status
#     track retries

# This keeps DB logic isolated.

from sqlalchemy.orm import Session

from backend.models.webhook_event import (
    WebhookEvent
)


class WebhookRepository:

    @staticmethod
    def create_event(
        db: Session,
        transaction_id: str,
        event_type: str
    ):

        event = WebhookEvent(
            transaction_id=transaction_id,
            event_type=event_type
        )

        db.add(event)

        db.commit()

        db.refresh(event)

        return event

    @staticmethod
    def update_delivery_status(
        db: Session,
        webhook_event: WebhookEvent,
        delivery_status: str,
        delivered: bool
    ):

        webhook_event.delivery_status = (
            delivery_status
        )

        webhook_event.delivered = delivered

        db.commit()