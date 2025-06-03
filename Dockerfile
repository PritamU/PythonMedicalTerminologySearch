# Base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies (includes pg_isready)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

COPY entrypoint.sh .
ENTRYPOINT ["./entrypoint.sh"]


# Expose Flask port
EXPOSE 5000

# Default command (used by docker-compose)
CMD ["sh", "-c", "./wait-for-postgres.sh db && python seed.py && flask run --host=0.0.0.0"]


