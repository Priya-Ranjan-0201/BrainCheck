# ============================================================
# Docker Compose Command Reference
# Dockerized Quiz Application
# ============================================================
#
# Docker Compose is a tool for defining and running
# multi-container Docker applications. For this project,
# it manages the Flask web service, SQLite named volume,
# environment variables, health checks, resource limits,
# and log rotation — all configured in docker-compose.yml.
#
# Why use Compose instead of raw "docker run"?
#   • One command replaces a long "docker run" with many flags
#   • Configuration is version-controlled in docker-compose.yml
#   • .env file is automatically loaded (no --env-file flag)
#   • Named volumes, networks, and restart policies are declared
#   • Easy to scale to multi-container setups (add a DB service)
#
# Prerequisites:
#   • Docker Desktop installed and running (includes Compose V2)
#   • Terminal open in the project root (Dockerized-Quiz-App/)
#   • .env file present with your configuration
#
# Note: Modern Docker uses "docker compose" (with a space).
#       The legacy "docker-compose" (with a hyphen) is
#       deprecated but still works.
# ============================================================


# ─────────────────────────────────────────────────────────────
# 1. BUILD THE SERVICES
# ─────────────────────────────────────────────────────────────
#
# Purpose:
#   Reads docker-compose.yml, locates every service with a
#   "build:" directive, and builds its Docker image. For this
#   project, it builds the "web" service from the Dockerfile.
#
# How it works:
#   1. Compose reads docker-compose.yml and resolves ${VAR}
#      references from the .env file
#   2. Sends the build context (filtered by .dockerignore)
#      to the Docker daemon
#   3. Executes the multi-stage Dockerfile
#   4. Tags the resulting image as "quizapp-pipeline:latest"
#
# When to use:
#   • First time setting up the project
#   • After changing the Dockerfile
#   • After modifying requirements.txt (new Python packages)
#   • After changing .dockerignore
#
# Flags explained:
#   --no-cache  →  Ignores the Docker layer cache and rebuilds
#                  every layer from scratch. Use when cached
#                  layers are stale (e.g., pip cached old packages).
#
#   --pull      →  Pulls the latest version of the base image
#                  (python:3.13-slim) before building. Ensures
#                  you have the newest security patches.

docker compose build

# Force a full rebuild from scratch:
docker compose build --no-cache

# Pull latest base image first, then build:
docker compose build --pull

# Build with verbose output to diagnose issues:
docker compose build --progress=plain


# ─────────────────────────────────────────────────────────────
# 2. START THE SERVICES
# ─────────────────────────────────────────────────────────────
#
# Purpose:
#   Creates containers, networks, and volumes as defined in
#   docker-compose.yml, then starts all services. If images
#   don't exist yet, Compose builds them automatically.
#
# What happens on "docker compose up":
#   1. Creates the "quizapp_sqlite_data" named volume (if missing)
#   2. Creates the default bridge network for the project
#   3. Builds the image (if it doesn't exist)
#   4. Creates the "quizapp_web" container
#   5. Mounts the volume at /app/instance
#   6. Injects environment variables from .env
#   7. Starts Flask → creates tables → seeds data
#   8. Begins healthcheck polling (every 30 seconds)
#
# After this command, open http://localhost:5000
#
# Flags explained:
#   -d              →  Detached mode: runs containers in the
#                      background and returns control to your
#                      terminal. Without -d, all logs stream
#                      to your terminal and Ctrl+C stops everything.
#
#   --build         →  Forces a rebuild of the image before
#                      starting. This is the flag you'll use
#                      most often during development — it picks
#                      up code changes you've made since the
#                      last build.
#
#   --force-recreate →  Removes and recreates containers even
#                       if their configuration hasn't changed.
#                       Useful when you've changed .env values
#                       (Compose doesn't detect .env changes as
#                       "configuration changes" by default).

# Start in detached mode (most common):
docker compose up -d

# Build first, then start (use after code changes):
docker compose up -d --build

# Start in foreground (logs stream to terminal):
docker compose up

# Force-recreate to pick up .env changes:
docker compose up -d --force-recreate

# Build + recreate (fresh start with code + config changes):
docker compose up -d --build --force-recreate


# ─────────────────────────────────────────────────────────────
# 3. STOP & REMOVE THE SERVICES
# ─────────────────────────────────────────────────────────────
#
# Purpose:
#   Stops all running containers, removes them, and removes
#   the project's default network. This is the clean way to
#   shut down — much better than "docker stop" + "docker rm"
#   for each container.
#
# What is removed:
#   ✅ Containers (quizapp_web)
#   ✅ Default network
#
# What is NOT removed (by default):
#   ✅ Named volumes (quiz_data) — your database is safe
#   ✅ Built images (quizapp-pipeline:latest)
#
# Flags explained:
#   -v          →  Also removes named volumes declared in the
#                  "volumes:" section of docker-compose.yml.
#                  ⚠️  THIS PERMANENTLY DELETES YOUR DATABASE.
#
#   --rmi all   →  Also removes all images built by Compose.
#                  Frees disk space but requires a rebuild next time.
#
#   --rmi local →  Only removes images without a custom tag.
#
#   -t N        →  Custom grace period in seconds. Default is 10.
#                  Increase if your app needs more time to shut down.

# Standard shutdown (keeps data and images):
docker compose down

# Shutdown AND delete the database volume:
# ⚠️ WARNING: This permanently destroys all quiz data!
docker compose down -v

# Shutdown AND remove built images:
docker compose down --rmi all

# Shutdown with a longer grace period (30 seconds):
docker compose down -t 30

# Full nuclear cleanup (removes everything):
# ⚠️ WARNING: Deletes database, images, and all state!
docker compose down -v --rmi all


# ─────────────────────────────────────────────────────────────
# 4. VIEW LOGS
# ─────────────────────────────────────────────────────────────
#
# Purpose:
#   Aggregates and displays stdout/stderr output from all
#   services. When running multiple services, each service's
#   output is color-coded with its name prefix.
#
# What to look for on healthy startup:
#   quizapp_web | * Serving Flask app 'app'
#   quizapp_web | * Running on http://0.0.0.0:5000
#
# What indicates a problem:
#   quizapp_web | Traceback (most recent call last):
#   quizapp_web | ImportError: No module named 'flask'
#   quizapp_web | sqlite3.OperationalError: unable to open database
#
# Flags explained:
#   -f          →  Follow mode: streams new log lines in real-time.
#                  Press Ctrl+C to stop following (doesn't stop
#                  the container — only detaches from log output).
#
#   --tail N    →  Shows only the last N lines. Without this flag,
#                  Compose shows the ENTIRE log history, which
#                  can be very long on a running deployment.
#
#   -t          →  Prepends ISO-8601 timestamps to each line.
#                  Useful for correlating events across services.
#
#   web         →  Filter to a specific service name (defined in
#                  docker-compose.yml). Without this, logs from
#                  ALL services are shown interleaved.

# Show all logs (may be very long):
docker compose logs

# Follow live output from all services:
docker compose logs -f

# Follow only the web service:
docker compose logs -f web

# Show last 50 lines:
docker compose logs --tail 50

# Show last 100 lines from web with timestamps:
docker compose logs --tail 100 -t web

# Show logs since a specific time:
docker compose logs --since "2026-07-11T12:00:00" web

# Show logs from the last 30 minutes:
docker compose logs --since 30m web


# ─────────────────────────────────────────────────────────────
# 5. RESTART THE SERVICES
# ─────────────────────────────────────────────────────────────
#
# Purpose:
#   Stops and restarts containers WITHOUT rebuilding images
#   or recreating the containers. This is a "soft restart" —
#   equivalent to stopping and starting the same container.
#
# When to use:
#   • Application is stuck or unresponsive
#   • You changed an environment variable in .env and want
#     to reload it (note: "restart" alone doesn't reload .env
#     — use "docker compose up -d --force-recreate" for that)
#   • After clearing the database manually
#
# When NOT to use:
#   • After changing application code → use "up -d --build"
#   • After changing the Dockerfile → use "build" then "up -d"
#   • After changing docker-compose.yml → use "up -d"
#
# Flags explained:
#   -t N    →  Grace period in seconds before force-kill.
#              Default: 10 seconds.
#   web     →  Restart only a specific service.

docker compose restart

# Restart only the web service:
docker compose restart web

# Restart with a longer grace period:
docker compose restart -t 30 web


# ─────────────────────────────────────────────────────────────
# 6. CHECK SERVICE STATUS
# ─────────────────────────────────────────────────────────────
#
# Purpose:
#   Shows the current state of all services defined in
#   docker-compose.yml, including health status, port
#   mappings, and whether containers are running.

docker compose ps

# Show status in a table format:
docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"

# Include stopped services:
docker compose ps -a


# ─────────────────────────────────────────────────────────────
# 7. EXECUTE COMMANDS INSIDE A SERVICE
# ─────────────────────────────────────────────────────────────
#
# Purpose:
#   Runs a command inside an already-running service container.
#   Useful for debugging, inspecting files, or running one-off
#   management tasks.
#
# "exec" vs "run":
#   exec  →  Runs inside the EXISTING container (shares state)
#   run   →  Creates a NEW container (isolated, no side effects)

# Open an interactive shell:
docker compose exec web /bin/bash

# Check who the container runs as:
docker compose exec web whoami
# → appuser

# Check the database file:
docker compose exec web ls -la /app/instance/

# Run a Python command:
docker compose exec web python -c "from app import create_app; print('OK')"

# Run a one-off command in a NEW disposable container:
docker compose run --rm web python -c "print('Hello from a temp container!')"


# ─────────────────────────────────────────────────────────────
# 8. VALIDATE CONFIGURATION
# ─────────────────────────────────────────────────────────────
#
# Purpose:
#   Parses docker-compose.yml, resolves all ${VAR} references
#   from .env, and prints the fully resolved configuration.
#   This is the best way to verify that environment variable
#   substitution is working correctly.

docker compose config

# Show only the service names:
docker compose config --services

# Show only the volumes:
docker compose config --volumes

# Check for syntax errors without showing output:
docker compose config --quiet


# ─────────────────────────────────────────────────────────────
# 9. RESOURCE MONITORING
# ─────────────────────────────────────────────────────────────
#
# Purpose:
#   Shows real-time resource consumption for all Compose
#   services — CPU, memory, network I/O, and process count.

# Show processes running inside each service:
docker compose top

# Live resource usage (from Docker directly):
docker stats quizapp_web

# One-shot resource snapshot:
docker stats --no-stream quizapp_web


# ─────────────────────────────────────────────────────────────
# 10. PAUSE & UNPAUSE
# ─────────────────────────────────────────────────────────────
#
# Purpose:
#   Freezes all processes in a container without stopping it.
#   Memory state is preserved — the container resumes instantly
#   when unpaused. Useful for temporarily freeing CPU/memory.
#
# Difference from stop:
#   pause   →  Freezes processes (instant resume)
#   stop    →  Terminates processes (cold start on restart)

docker compose pause
docker compose unpause


# ─────────────────────────────────────────────────────────────
# COMMON WORKFLOWS — QUICK REFERENCE
# ─────────────────────────────────────────────────────────────

# ── First-time setup ────────────────────────────────────────
#   cp .env.example .env         # Configure environment
#   docker compose up -d --build # Build and start

# ── Daily development (after code changes) ──────────────────
#   docker compose up -d --build

# ── Check status and health ─────────────────────────────────
#   docker compose ps
#   docker compose logs --tail 20 web

# ── Debug a problem ─────────────────────────────────────────
#   docker compose logs -f web           # Watch live logs
#   docker compose exec web /bin/bash    # Shell into container
#   docker compose restart web           # Restart if stuck

# ── Update .env variables ──────────────────────────────────
#   # Edit .env file, then:
#   docker compose up -d --force-recreate

# ── Complete teardown ───────────────────────────────────────
#   docker compose down                  # Keep database
#   docker compose down -v               # Delete database too

# ── Full clean slate (start fresh) ──────────────────────────
#   docker compose down -v --rmi all
#   docker compose up -d --build
