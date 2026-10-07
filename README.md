# Dabbewala API

A FastAPI and SQLModel service for managing delivery orders and generating order summaries.

## Features

- Create, list, retrieve, update, and delete orders.
- Filter orders by status, creation date, and pagination.
- Generate status-based order summary statistics.
- Automatically create the SQLite database tables on application startup.
- Uses timezone-aware datetime values for order timestamps.

## Technology Stack

- FastAPI for the API and dependency injection.
- SQLModel for ORM models and database queries.
- SQLite for local persistence.
- Uvicorn for running the application.

## Requirements

- Python 3.10 or newer
- `venv` is recommended for isolating dependencies.

## Installation

```bash
python -m venv venv
venv/Scripts/activate
python -m pip install -r requirements.txt
```

On Linux or macOS, activate the environment with:

```bash
source venv/bin/activate
```

## Run the application

```bash
uvicorn main:app --reload
```

Open the API documentation at:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

The application creates `dabbewala.db` automatically during startup.

## API Endpoints

### Root

```http
GET /
```

Returns a welcome message.

### Create an order

```http
POST /orders/create
Content-Type: application/json
```

Request body:

```json
{
  "customer_name": "Ananya Rao",
  "delivery_address": "12 Main Road, Mysore",
  "items": "Tea and sweets"
}
```

### List orders

```http
GET /orders/?status=preparing&created_date=2026-10-07&skip=0&limit=10
```

Optional query parameters:

- `status`: `preparing`, `picked_up`, `in_transit`, or `delivered`
- `created_date`: date in `YYYY-MM-DD` format
- `skip`: number of records to skip
- `limit`: maximum number of records, from 1 to 100

### Get one order

```http
GET /orders/{order_id}
```

### Update an order

```http
PATCH /orders/{order_id}
Content-Type: application/json
```

Example body:

```json
{
  "status": "in_transit",
  "delivery_address": "13 Main Road, Mysore"
}
```

### Delete an order

```http
DELETE /orders/{order_id}
```

### Get an order summary

```http
GET /order_summary/?summary_date=2026-10-07
```

The `summary_date` parameter is optional. If omitted, the current UTC date is used.

The response contains:

- Total number of orders.
- Counts for each order status.
- The selected date.

## Example

```bash
curl -X POST http://127.0.0.1:8000/orders/create \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Ananya Rao",
    "delivery_address": "12 Main Road, Mysore",
    "items": "Tea and sweets"
  }'
```

## Project Structure

```text
.
├── database.py
├── main.py
├── models.py
├── requirements.txt
└── routes/
    ├── orders.py
    └── stats.py
```

## Notes

- The database file is stored as `dabbewala.db` in the project root.
- The application uses an in-memory SQLModel metadata registry for schema creation.
- Date filters are interpreted in UTC.
