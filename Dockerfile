# Python image to use
FROM python:3.11-slim

# Directory where all the next commands are going to execute
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (origin / -> destination "/app")
COPY . .

# Expose port
EXPOSE 8000

# Run migrations and then the application
CMD sh -c "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"
