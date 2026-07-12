# BrainCheck - Production Dockerfile
# Multi-stage build: compile deps in stage 1, run lean in stage 2

# ── Stage 1: Builder ──────────────────────────────────────────
# Install build toolchain and compile Python dependencies into
# an isolated virtualenv so only runtime artifacts carry over.
# ──────────────────────────────────────────────────────────────
FROM python:3.13-slim AS builder

WORKDIR /build

# Prevent .pyc file creation and ensure real-time log output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install OS-level build dependencies required by some Python
# packages (e.g. wheels with C extensions), then clean the
# apt cache to keep the layer small.
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first (Docker layer-caching optimisation).
# Only re-installs if requirements.txt changes.
COPY requirements.txt .

# Create a virtualenv and install all production dependencies.
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt


# ── Stage 2: Final (runtime) ─────────────────────────────────
# Slim runtime image with no compilers, no caches, and a
# non-root user for defense-in-depth.
# ──────────────────────────────────────────────────────────────
FROM python:3.13-slim AS final

# OCI / Docker metadata labels
LABEL maintainer="PRIYE RANJAN" \
      description="BrainCheck Flask BrainCheck" \
      version="1.0.0"

WORKDIR /app

# Runtime environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    FLASK_APP="app.py" \
    FLASK_ENV="production" \
    PORT=5000

# ── Non-root user (security best practice) ───────────────────
# Running as root inside a container is an unnecessary risk.
RUN groupadd --system appgroup && \
    useradd  --system --gid appgroup --create-home appuser

# Bring the pre-built virtualenv from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy application source code
COPY . .

# Create the SQLite instance directory with correct ownership.
# Only the appuser needs write access for the database file.
RUN mkdir -p instance && \
    chown -R appuser:appgroup instance

# Drop to non-root for all subsequent commands and runtime
USER appuser

# Expose the Flask server port
EXPOSE ${PORT}

# ── Healthcheck ──────────────────────────────────────────────
# Docker (and orchestrators like Compose / Swarm) will
# periodically hit this endpoint to verify the app is alive.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${PORT}/')" || exit 1

# ── Entrypoint ───────────────────────────────────────────────
# Start the Flask development server bound to 0.0.0.0 so it
# is reachable from outside the container.
# For true production use, swap to: gunicorn -b 0.0.0.0:5000 "app:create_app()"
CMD ["python", "app.py"]
