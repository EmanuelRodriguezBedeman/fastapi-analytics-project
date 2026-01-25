# FastAPI Analytics Project

[App on Render](https://fastapi-analytics-project.onrender.com/docs)

A modern e-commerce API built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features

- User authentication and authorization
- Product management
- Order processing
- Payment integration
- RESTful API design
- Database migrations with Alembic
- Docker support
- CI/CD with GitHub Actions

## Project Structure

```
fastapi-ecommerce/
├── app/
│   ├── models/          # SQLAlchemy database models
│   ├── schemas/         # Pydantic schemas for validation
│   ├── routers/         # API route handlers
│   ├── services/        # Business logic services
│   └── utils/           # Utility functions and dependencies
├── tests/               # Test suite
├── alembic/             # Database migrations
└── .github/workflows/   # CI/CD workflows
```

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Docker (optional)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fastapi-ecommerce
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials and settings
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Start the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation will be available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Running Tests

```bash
pytest tests/ -v
```

## Docker

Build and run with Docker:

```bash
docker build -t fastapi-ecommerce .
docker run -p 8000:8000 fastapi-ecommerce
```

## License

MIT
