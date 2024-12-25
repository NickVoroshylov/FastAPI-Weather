FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry \
    && poetry install --no-interaction --no-dev

COPY . /app/

EXPOSE 5000