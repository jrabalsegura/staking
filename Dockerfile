# Use the official Python 3.11 slim image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (if any)
RUN apt-get update && apt-get install -y && apt-get install -y awscli  \
    build-essential

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy only pyproject.toml and poetry.lock to leverage Docker cache
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application code
COPY . .

# RUN poetry run python stakes_manager/manage.py collectstatic --noinput

# Expose the port Gunicorn will run on!
EXPOSE 8001

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=stakes_manager.settings

# Run Gunicorn
CMD ["gunicorn", "--chdir", "stakes_manager", "stakes_manager.wsgi:application", "--bind", "127.0.0.1:8001", "--workers", "3"]