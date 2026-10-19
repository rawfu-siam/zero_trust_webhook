# ==============================================================================
# Multi-Stage Production-Grade Dockerfile Matrix
# Employs high-velocity dependency resolution via uv and zero-trust user privileges.
# ==============================================================================

# Stage 1: Dependency compilation and locking engine stage
FROM python:3.11-slim AS builder

# Establish structural engine system path contexts
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/app/.venv

WORKDIR /app

# Safely inject the high-velocity uv binary onto our compilation fabric
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Mount package definition sheets and pull pinned environment matrices rapidly
COPY requirements.txt .
RUN uv venv /app/.venv && \
    uv pip install --no-cache -r requirements.txt

# Stage 2: Low-footprint secure application execution layer
FROM python:3.11-slim AS runner

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Create a restricted application group and user profile to guarantee zero-root safety bounds
RUN groupadd -g 10001 agency_workers && \
    useradd -u 10001 -g agency_workers -m -s /sbin/nologin agency_user

# Pull the compiled static virtual environment boundaries out of the compiler stage
COPY --from=builder /app/.venv /app/.venv
COPY src/ /app/src/

# Provision explicit access rights to application directory matrices before shifting identities
RUN chown -R agency_user:agency_workers /app

# Shift operating roles down to our unprivileged background daemon worker
USER agency_user

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
