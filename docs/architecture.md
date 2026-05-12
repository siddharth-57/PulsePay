# PulsePay Architecture

# This file explains:

How the entire system works
Major system components
Service responsibilities
Infrastructure design

## Goal

PulsePay is a distributed payment processing infrastructure designed to simulate production-grade fintech backend systems.

The system focuses on:

- async transaction processing
- fault tolerance
- retry-safe workflows
- idempotent APIs
- event-driven architecture
- transactional consistency

---

# High Level Architecture

Client
    ↓
FastAPI API Layer
    ↓
Payment Service
    ↓
PostgreSQL (Source of Truth)

Payment Service
    ↓
Redis Queue
    ↓
Celery Workers
    ↓
Payment Processing Engine

Event System
    ↓
Webhook Delivery
Notification Service

---

# Core Components

## API Layer

Responsible for:
- request validation
- idempotency handling
- request tracing
- authentication (future)

## Payment Service

Responsible for:
- payment creation
- transaction state management
- event publishing
- refund orchestration

## PostgreSQL

Primary source of truth.

Stores:
- transactions
- payment attempts
- audit logs
- webhook logs
- idempotency keys

## Redis

Used for:
- async queues
- retry queues
- event transport

## Celery Workers

Responsible for:
- background payment processing
- retries
- webhook delivery
- notifications