# ============================================================
# Docker Compose Commands Reference
# Dockerized Quiz Application
# ============================================================
#
# Docker Compose orchestrates multi-container applications
# defined in docker-compose.yml. For this project it manages
# the Flask web service, named volumes, environment variables,
# networking, and health checks — all in a single command.
#
# Prerequisites:
#   • Docker Desktop installed and running (includes Compose)
#   • Terminal open in the project root (Dockerized-Quiz-App/)
#   • .env file present with your configuration
#
# Note: Modern Docker uses `docker compose` (no hyphen).
#       The legacy `docker-compose` (hyphenated) still works
#       but is deprecated.
# ============================================================


# ─────────────────────────────────────────────────────────────
# 1. BUILD THE SERVICES
# ─────────────────────────────────────────────────────────────
#
# What it does:
#   Reads docker-compose.yml, finds every service with a
#   "build:" directive, and builds its Docker image.
#   Equivalent to running "docker build" for each service,
#   but Compose handles the context, tags, and caching.
#
#   --no-cache  →  Forces a full rebuild (ignores layer cache)
#   --pull      →  Always pull the latest base image first
#
# When to use:
#   • First time setting up the project
#   • After changing Dockerfile or requirements.txt
#   • After adding new Python dependencies

docker compose build

# Force a clean rebuild from scratch:
docker compose build --no-cache

# Pull latest base image before building:
docker compose build --pull


# ─────────────────────────────────────────────────────────────
# 2. START THE SERVICES
# ─────────────────────────────────────────────────────────────
#
# What it does:
#   Creates and starts all containers defined in
#   docker-compose.yml. If images don't exist yet, Compose
#   builds them automatically first.
#
#   -d          →  Detached mode (runs in background)
#   --build     →  Rebuild images before starting (useful
#                   when source code changed)
#   --force-recreate
#               →  Recreate containers even if config hasn't
#                   changed (picks up new env vars)
#
# After this command, open http://localhost:5000 in your browser.

docker compose up -d

# Build + start in one step (most common during development):
docker compose up -d --build

# Start in foreground (logs stream to terminal, Ctrl+C stops):
docker compose up

# Force-recreate containers (picks up .env changes):
docker compose up -d --force-recreate


# ─────────────────────────────────────────────────────────────
# 3. STOP & REMOVE THE SERVICES
# ─────────────────────────────────────────────────────────────
#
# What it does:
#   Stops all running containers and removes them, along
#   with the default network Compose created.
#
#   ⚠  Named volumes are NOT removed by default.
#      Your SQLite database (quiz_data) is safe.
#
#   -v          →  Also remove named volumes (⚠ DELETES DATA)
#   --rmi all   →  Also remove the built images
#   -t 10       →  Grace period in seconds before force-kill

docker compose down

# Stop and DELETE the database volume (⚠ destroys all data):
docker compose down -v

# Stop, remove containers AND images:
docker compose down --rmi all

# Stop with a custom grace period (30 seconds):
docker compose down -t 30


# ─────────────────────────────────────────────────────────────
# 4. VIEW LOGS
# ─────────────────────────────────────────────────────────────
#
# What it does:
#   Aggregates and displays stdout/stderr from all services.
#   Color-coded by service name for easy reading.
#
#   -f          →  Follow (live tail, streams new output)
#   --tail 100  →  Show only the last 100 lines
#   web         →  Filter to a specific service name
#
# Press Ctrl+C to stop following.

docker compose logs

# Follow live output from all services:
docker compose logs -f

# Follow only the web service:
docker compose logs -f web

# Show last 50 lines:
docker compose logs --tail 50

# Show logs with timestamps:
docker compose logs -f -t web


# ─────────────────────────────────────────────────────────────
# 5. RESTART THE SERVICES
# ─────────────────────────────────────────────────────────────
#
# What it does:
#   Stops and restarts containers WITHOUT rebuilding images
#   or recreating containers. Useful when the app is stuck
#   or you need to reload environment variables.
#
#   -t 10  →  Grace period before force-kill (default: 10)
#   web    →  Restart only a specific service
#
# ⚠  "restart" does NOT pick up Dockerfile or code changes.
#    Use "docker compose up -d --build" for that.

docker compose restart

# Restart only the web service:
docker compose restart web

# Restart with a custom timeout:
docker compose restart -t 30 web


# ─────────────────────────────────────────────────────────────
# BONUS: ADDITIONAL COMPOSE COMMANDS
# ─────────────────────────────────────────────────────────────

# Check the status of all services:
docker compose ps

# Check service health status:
docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"

# Execute a command inside a running service:
docker compose exec web /bin/bash

# Run a one-off command in a new container (doesn't affect running service):
docker compose run --rm web python -c "print('Hello from container!')"

# Validate and view the resolved docker-compose.yml:
docker compose config

# Pull the latest base images (before building):
docker compose pull

# Pause all containers (freeze without stopping):
docker compose pause

# Unpause frozen containers:
docker compose unpause

# View resource usage for all services:
docker compose top


# ─────────────────────────────────────────────────────────────
# QUICK REFERENCE – COMMON WORKFLOWS
# ─────────────────────────────────────────────────────────────
#
# First-time setup:
#   docker compose up -d --build
#
# Daily development (code changed):
#   docker compose up -d --build
#
# View what's happening:
#   docker compose ps
#   docker compose logs -f web
#
# Something went wrong:
#   docker compose restart web
#   docker compose logs --tail 50 web
#
# Tear down everything:
#   docker compose down
#
# Full clean slate (⚠ deletes database):
#   docker compose down -v --rmi all
#   docker compose up -d --build
