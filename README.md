# PulsePay

PulsePay is a production-inspired payment processing backend built using FastAPI, PostgreSQL, Redis, Celery, and Docker.

The project demonstrates how modern payment platforms handle transaction processing, authentication, authorization, idempotency, background job execution, audit logging, metrics collection, and infrastructure monitoring.

---

## Features

### Payment Processing

* Create and retrieve payment transactions
* Transaction status tracking
* Retry handling for failed transactions

### Authentication & Authorization

* User registration
* Secure password hashing using bcrypt
* JWT-based authentication
* Role-based access control (RBAC)
* Admin-only endpoints

### Reliability & Scalability

* Idempotency protection to prevent duplicate payments
* Background payment processing using Celery
* Redis-backed task queues
* Webhook event processing

### Monitoring & Observability

* Transaction metrics
* Audit logging
* Request tracing with unique request IDs
* Health checks
* Readiness checks
* Docker container health checks

### Security

* JWT authentication
* Password hashing
* API rate limiting
* Environment-based configuration

### Infrastructure

* Dockerized services
* PostgreSQL database
* Redis message broker
* Automated database migrations with Alembic

### Testing

* Automated test suite using Pytest
* Authentication testing
* Transaction testing
* Idempotency testing
* Metrics testing
* Worker testing

---

## Architecture

```text
                ┌─────────────┐
                │   Client    │
                └──────┬──────┘
                       │
                       ▼
              ┌─────────────────┐
              │     FastAPI     │
              └──────┬──────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
         ▼           ▼           ▼

 ┌────────────┐ ┌─────────┐ ┌──────────────┐
 │ PostgreSQL │ │  Redis  │ │ JWT Auth/RBAC│
 └────────────┘ └────┬────┘ └──────────────┘
                     │
                     ▼

              ┌─────────────┐
              │   Celery    │
              │   Workers   │
              └──────┬──────┘
                     │
         ┌───────────┴───────────┐
         ▼                       ▼

 ┌────────────────┐    ┌────────────────┐
 │ Payment Worker │    │ Webhook Worker │
 └────────────────┘    └────────────────┘
```

---

## Tech Stack

### Backend

* FastAPI
* SQLAlchemy
* Alembic
* Pydantic

### Database

* PostgreSQL

### Queue & Caching

* Redis
* Celery

### Authentication

* JWT
* bcrypt
* Passlib

### Infrastructure

* Docker
* Docker Compose

### Testing

* Pytest

---

## API Endpoints

### Authentication

| Method | Endpoint       |
| ------ | -------------- |
| POST   | `/users/`      |
| POST   | `/users/login` |
| GET    | `/users/me`    |

### Transactions

| Method | Endpoint                         |
| ------ | -------------------------------- |
| POST   | `/transactions/`                 |
| GET    | `/transactions/{transaction_id}` |

### Metrics

| Method | Endpoint    |
| ------ | ----------- |
| GET    | `/metrics/` |

### Monitoring

| Method | Endpoint  |
| ------ | --------- |
| GET    | `/health` |
| GET    | `/ready`  |

---

## Running Locally

### Clone Repository

```bash
git clone <repository-url>
cd PulsePay
```

### Configure Environment

Create a `.env` file:

```env
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/pulsepay
REDIS_URL=redis://redis:6379/0

JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60
```

### Start Infrastructure

```bash
docker compose up -d --build
```

### Run Database Migrations

```bash
alembic upgrade head
```

### Access API

Swagger UI:

```text
http://localhost:8000/docs
```

---

## Testing

Run all tests:

```bash
pytest -v
```

---

## Key Engineering Concepts Demonstrated

* REST API Design
* JWT Authentication
* Role-Based Access Control
* Payment Processing Workflows
* Idempotency
* Background Job Processing
* Distributed Systems Concepts
* Audit Logging
* Metrics Collection
* Rate Limiting
* Dockerized Infrastructure
* Database Migrations
* Automated Testing

---

## Future Improvements

* Payment Gateway Integration (Stripe/Razorpay)
* API Versioning
* CI/CD Pipeline
* Kubernetes Deployment
* Prometheus Metrics
* Grafana Dashboards
* OpenTelemetry Tracing

---

## Author

Siddharth Chaudhari

Built as a backend engineering project to demonstrate production-grade software development practices and distributed systems concepts.
