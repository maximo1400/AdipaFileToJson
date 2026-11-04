FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Enable bytecode compilation and fast copy mode
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Cache dependency layers
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# Copy backend application source
COPY . .

# Final sync without dev dependencies
RUN uv sync --frozen --no-dev

# Ensure virtualenv binaries are in PATH
ENV PATH="/app/.venv/bin:$PATH"

# Default port (Render injects $PORT environment variable)
ENV PORT=8000
EXPOSE 8000

# Start Uvicorn server
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
