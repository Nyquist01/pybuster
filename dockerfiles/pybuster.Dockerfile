FROM astral/uv:python3.12-bookworm-slim AS builder

WORKDIR /app

COPY backend ./

RUN uv sync

EXPOSE 8000
