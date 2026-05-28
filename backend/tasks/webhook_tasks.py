# What This Step Does: Creates async webhook delivery worker.

# This simulates:
#     external HTTP callbacks
#     webhook delivery
#     external integrations

# This is a HUGE fintech/backend concept.
# There are 2 different queues for making payments and for webhook and different workers listening to these queues

import random
import time

from backend.core.celery_app import celery_app

from backend.core.database import SessionLocal

from backend.models.webhook_event import (
    WebhookEvent
)

from backend.core.logger import logger

@celery_app.task
def send_webhook_task(
    webhook_event_id: str
):

    db = SessionLocal()

    try:

        webhook_event = (
            db.query(WebhookEvent)
            .filter(
                WebhookEvent.id == webhook_event_id
            )
            .first()
        )

        if not webhook_event:
            return

        logger.info(
            f"Sending webhook for transaction "
            f"{webhook_event.transaction_id}"
        )

        time.sleep(3)

        success = random.choice(
            [
                True,
                False
            ]
        )

        if success:

            webhook_event.delivery_status = (
                "DELIVERED"
            )

            webhook_event.delivered = True

            db.commit()

            logger.info(
                f"Webhook delivered successfully"
            )

        else:

            webhook_event.delivery_status = (
                "FAILED"
            )

            webhook_event.retry_count += 1

            db.commit()

            logger.info(
                f"Webhook delivery failed"
            )

    finally:

        db.close()