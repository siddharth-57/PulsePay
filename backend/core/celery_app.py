# Creates centralized Celery application configuration.
# This file connects:
#     Celery
#     Redis
#     async task processing

# All background workers will use this.

from celery import Celery

from backend.core.config import settings


celery_app = Celery(
    "pulsepay",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "backend.tasks.payment_tasks",      #this imports task modules so celery can execute them
        "backend.tasks.webhook_tasks"       #Register Webhook Tasks In Celery, Allows Celery to discover webhook tasks. 
    ]
)


celery_app.conf.task_routes = {
    "backend.tasks.payment_tasks.*": {
        "queue": "payment_queue"
    },

    "backend.tasks.webhook_tasks.*": {
        "queue": "webhook_queue"
    }
}