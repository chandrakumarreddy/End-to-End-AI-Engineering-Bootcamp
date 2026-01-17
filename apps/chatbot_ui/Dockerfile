# Builder stage
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
WORKDIR /app

ENV UV_COMPILE_BYTECODE=1

# Copy dependency files
COPY pyproject.toml uv.lock ./

COPY apps/chatbot_ui ./apps/chatbot_ui

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --package chatbot_ui

ENV PYTHONOPTIMIZE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/apps/chatbot_ui/src:$PYTHONPATH"

RUN addgroup --system app && \
    adduser --system --ingroup app --home /home/app app && \
    chown -R app:app /app

USER app

ENV HOME=/home/app

EXPOSE 3000

WORKDIR /app/apps/chatbot_ui/src

CMD ["uv", "run", "streamlit", "run", "chatbot_ui/app.py", "--server.port", "3000", "--server.address", "0.0.0.0"]
