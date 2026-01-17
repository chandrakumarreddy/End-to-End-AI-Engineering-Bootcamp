# Builder stage
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
WORKDIR /app

ENV UV_COMPILE_BYTECODE=1

# set python dir to src
ENV PYTHONPATH="/app/src/api/src:$PYTHONPATH"

# Copy dependency files
COPY pyproject.toml uv.lock ./

COPY apps/api ./apps/api

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --package api

ENV PYTHONOPTIMIZE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/apps/api/src:$PYTHONPATH"

RUN addgroup --system app && \
    adduser --system --ingroup app app && \
    chown -R app:app /app

USER app

EXPOSE 8000

WORKDIR /app/apps/api/src

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
