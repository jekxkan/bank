FROM python:3.11.7-slim-bookworm

ENV POETRY_VERSION=1.7.1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    ENV=dev

RUN pip install "poetry==$POETRY_VERSION" \
    debugpy

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN POETRY_VIRTUALENVS_CREATE=false poetry install

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]