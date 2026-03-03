# BookStore Microservice System - Assignment 05

## Architecture

This project decomposes a monolithic BookStore into **12 independent microservices** using Django REST Framework, orchestrated with Docker Compose.

## Services

| Service | Port | Description |
|---------|------|-------------|
| api-gateway | 8000 | Web interface routing to all services |
| customer-service | 8001 | Customer CRUD, auto-creates cart |
| staff-service | 8002 | Staff management |
| manager-service | 8003 | Manager management |
| catalog-service | 8004 | Category management |
| book-service | 8005 | Book CRUD |
| cart-service | 8006 | Cart & cart items management |
| order-service | 8007 | Order creation, triggers pay & ship |
| pay-service | 8008 | Payment processing |
| ship-service | 8009 | Shipping processing |
| comment-rate-service | 8010 | Book reviews & ratings |
| recommender-ai-service | 8011 | Book recommendations |

## Functional Requirements

1. **Customer registration** → auto-creates a cart (customer-service → cart-service)
2. **Staff manages books** → CRUD via book-service
3. **Customer cart operations** → add/view/update items (cart-service → book-service validation)
4. **Order placement** → triggers payment and shipping (order-service → pay-service, ship-service)
5. **Book ratings** → customers rate/review books (comment-rate-service → book-service)

## Inter-Service Communication

```
customer-service --POST /carts/--> cart-service
cart-service --GET /books/{id}/--> book-service
order-service --GET /carts/{id}/--> cart-service
order-service --POST /payments/--> pay-service
order-service --POST /shipments/--> ship-service
comment-rate-service --GET /books/{id}/--> book-service
recommender-ai-service --GET /reviews/top-rated/--> comment-rate-service
recommender-ai-service --GET /books/{id}/--> book-service
```

## Quick Start

```bash
docker-compose up --build
```

Then visit: http://localhost:8000

## Tech Stack

- **Framework**: Django REST Framework
- **Language**: Python 3.11
- **Database**: SQLite (independent per service)
- **Container**: Docker + Docker Compose
- **Communication**: REST (synchronous)
