# Dockerfile
ARG PYTHON_VERSION=3.9

FROM python:${PYTHON_VERSION}-alpine AS builder

WORKDIR /app

RUN apk update && apk add --no-cache \
    build-base \
    libffi-dev \
    musl-dev \
    postgresql-dev \
    gcc \
    python3-dev \
    linux-headers \
    && rm -rf /var/cache/apk/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:${PYTHON_VERSION}-alpine

ARG DEV_MODE=false
ENV DEV_MODE=$DEV_MODE

WORKDIR /app

# Instalamos librerías necesarias y postgresql-client para pg_isready
RUN apk add --no-cache libpq libffi postgresql-client && rm -rf /var/cache/apk/*

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY . .

# Entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV PYTHONPATH=/app
ENV ALEMBIC_CONFIG=/app/alembic.ini

EXPOSE 8000

CMD ["/entrypoint.sh"]
