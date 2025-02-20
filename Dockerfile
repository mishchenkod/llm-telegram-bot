# Use Python 3.13 image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Disable Poetry virtual environment in Docker as containers provide isolation
RUN poetry config virtualenvs.create false

# Copy dependency files for caching - Docker will only rebuild dependencies if these change
COPY poetry.lock pyproject.toml .

# Install dependencies
RUN poetry install --no-interaction --no-ansi --only main

# Copy project
COPY . .

# Start application
CMD ["python", "main.py"]