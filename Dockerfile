FROM python:3.13-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --upgrade pip && pip install poetry

# Working directory
WORKDIR /app

# Copy only dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies WITHOUT current project
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Copy entire project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run gunicorn in production
CMD ["poetry", "run", "gunicorn", "Enigma.wsgi:application", "--bind", "0.0.0.0:8000"]
