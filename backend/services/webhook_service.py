# Create Webhook Service
# What This Step Does: Creates orchestration layer for webhook generation.
# This separates: business logic from task dispatching

from sqlalchemy.orm import Session

from backend.repositories.webhook_repository import (
    WebhookRepository
)

from backend.tasks.webhook_tasks import (
    send_webhook_task
)


class WebhookService:

    @staticmethod
    def create_webhook_event(
        db: Session,
        transaction_id: str,
        event_type: str
    ):

        webhook_event = (
            WebhookRepository.create_event(
                db=db,
                transaction_id=transaction_id,
                event_type=event_type
            )
        )

        send_webhook_task.delay(
            webhook_event.id
        )

        return webhook_event