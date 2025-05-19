FROM python:3.13.0-slim-bookworm AS builder

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install --no-cache-dir uv && \
    uv sync --no-dev && \
    rm -rf /root/.cache/pip

FROM python:3.13.0-slim-bookworm AS runtime

WORKDIR /app

COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

COPY app/ app/

COPY migrations/ migrations/

COPY main.py .

ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

