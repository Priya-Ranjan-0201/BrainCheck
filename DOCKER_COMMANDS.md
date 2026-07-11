# ============================================================
# Docker CLI Command Reference
# Dockerized Quiz Application
# ============================================================
#
# A complete guide to building, running, inspecting, and
# managing the Quiz App container using the Docker CLI.
#
# Prerequisites:
#   • Docker Desktop installed and running
#   • Terminal open in the project root (Dockerized-Quiz-App/)
#   • .env file configured with your settings
#
# Image name: quizapp-pipeline:latest
# Container name: quizapp_web
# ============================================================


# ─────────────────────────────────────────────────────────────
# 1. BUILD THE DOCKER IMAGE
# ─────────────────────────────────────────────────────────────
#
# Purpose:
#   Reads the Dockerfile instruction-by-instruction, executes
#   each layer, and produces a tagged image stored locally on
#   your machine. The image is a self-contained package of
#   your application with all its dependencies.
#
# How it works:
#   1. Docker reads .dockerignore to filter the build context
#   2. Stage 1 (builder): installs build-essential, creates a
#      virtualenv, and installs requirements.txt
#   3. Stage 2 (final): copies only the virtualenv and source
#      code into a clean python:3.13-slim image
#   4. Creates the appuser for non-root execution
#
# Flags explained:
#   -t  →  Tags the image with a name:version label.
#          Without a tag, the image only has a hash ID.
#   .   →  Build context: the current directory. Docker sends
#          all non-ignored files to the Docker daemon.
#
# Timing:
#   First build: ~1-3 minutes (downloads base image + installs)
#   Subsequent builds: ~10-30 seconds (Docker layer caching)

docker build -t quizapp-pipeline:latest .

# Force a full rebuild without cache (useful after dependency changes):
docker build --no-cache -t quizapp-pipeline:latest .

# Build with progress output (see each layer):
docker build --progress=plain -t quizapp-pipeline:latest .


# ─────────────────────────────────────────────────────────────
# 2. VERIFY THE IMAGE WAS CREATED
# ─────────────────────────────────────────────────────────────
#
# Purpose:
#   Confirms the image exists locally and shows its metadata.
#   This is the first thing to check after a build.
#
# What to look for:
#   REPOSITORY        TAG       IMAGE ID       SIZE
#   quizapp-pipeline  latest    abc123def456   ~150 MB
#
#   • Size should be under 200 MB (slim base, no dev deps)
#   • TAG should be "latest" (or your custom tag)
#   • CREATED should show a recent timestamp

docker images

# Filter to only show your application image:
docker images quizapp-pipeline

# Show image details in a custom format:
docker images quizapp-pipeline --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedSince}}"

# Inspect the full image metadata (layers, env vars, labels):
docker inspect quizapp-pipeline:latest


# ─────────────────────────────────────────────────────────────
# 3. RUN THE CONTAINER
# ─────────────────────────────────────────────────────────────
#
# Purpose:
#   Creates a new container from the image and starts it.
#   A container is a running instance of an image — like
#   launching an .exe from an installer.
#
# What happens on startup:
#   1. Docker creates an isolated filesystem from the image
#   2. Mounts the quiz_data volume at /app/instance
#   3. Loads environment variables from .env
#   4. Runs "python app.py" as the appuser
#   5. Flask creates database tables and seeds default data
#   6. Flask starts listening on 0.0.0.0:5000
#
# Flags explained:
#   -d                  →  Detached mode: runs in the background.
#                          Without -d, logs stream to your terminal
#                          and Ctrl+C stops the container.
#
#   --name quizapp_web  →  Human-readable name for the container.
#                          Without this, Docker assigns a random name
#                          like "jovial_einstein".
#
#   -p 5000:5000        →  Port mapping (host_port:container_port).
#                          Maps your machine's port 5000 to the
#                          container's port 5000. Use -p 8080:5000
#                          to access the app on port 8080 instead.
#
#   -v quiz_data:/app/instance
#                       →  Named volume mount. Docker manages the
#                          storage location. The SQLite database file
#                          lives here and survives container removal.
#
#   --restart unless-stopped
#                       →  Restart policy:
#                          • Container auto-restarts on crash
#                          • Container auto-starts on Docker boot
#                          • Only stays stopped if YOU stop it
#
#   --env-file .env     →  Loads all KEY=VALUE pairs from .env as
#                          environment variables inside the container.
#
# After running, open http://localhost:5000 in your browser.

docker run -d \
  --name quizapp_web \
  -p 5000:5000 \
  -v quiz_data:/app/instance \
  --restart unless-stopped \
  --env-file .env \
  quizapp-pipeline:latest

# PowerShell equivalent (use backtick for line continuation):
# docker run -d `
#   --name quizapp_web `
#   -p 5000:5000 `
#   -v quiz_data:/app/instance `
#   --restart unless-stopped `
#   --env-file .env `
#   quizapp-pipeline:latest

# Run in foreground (see logs directly, Ctrl+C to stop):
docker run \
  --name quizapp_web \
  -p 5000:5000 \
  -v quiz_data:/app/instance \
  --env-file .env \
  quizapp-pipeline:latest


# ─────────────────────────────────────────────────────────────
# 4. CHECK RUNNING CONTAINERS
# ─────────────────────────────────────────────────────────────
#
# Purpose:
#   Shows all currently running containers with their status,
#   port mappings, uptime, and health state.
#
# What to look for:
#   CONTAINER ID  NAME          STATUS                    PORTS
#   abc123        quizapp_web   Up 5 minutes (healthy)    0.0.0.0:5000->5000/tcp
#
#   STATUS meanings:
#     "Up X minutes"         →  Container is running
#     "Up X minutes (healthy)" →  Running AND healthcheck passing
#     "Exited (1)"           →  Container crashed (check logs)
#     "Restarting"           →  Container is in a crash loop
#
#   PORTS:
#     "0.0.0.0:5000->5000/tcp" →  Correctly mapped

docker ps

# Include stopped/exited containers:
docker ps -a

# Custom format for cleaner output:
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Show only container IDs (useful for scripting):
docker ps -q


# ─────────────────────────────────────────────────────────────
# 5. VIEW CONTAINER LOGS
# ─────────────────────────────────────────────────────────────
#
# Purpose:
#   Streams stdout/stderr output from the Flask application.
#   This is your primary debugging tool — every print()
#   statement, Flask request log, and Python traceback appears here.
#
# What to look for on healthy startup:
#   * Serving Flask app 'app'
#   * Running on http://0.0.0.0:5000
#   (no Python tracebacks or import errors)
#
# Flags explained:
#   -f          →  Follow mode: streams new log lines in real-time
#                  (like "tail -f" on Linux). Press Ctrl+C to stop.
#
#   --tail N    →  Shows only the last N lines. Useful when the
#                  log history is very long and you only need
#                  the most recent output.
#
#   -t          →  Prepends timestamps to each log line.
#
#   --since 1h  →  Shows only logs from the last 1 hour.

docker logs quizapp_web

# Follow live output (most commonly used):
docker logs -f quizapp_web

# Show last 50 lines with timestamps:
docker logs --tail 50 -t quizapp_web

# Show logs from the last hour:
docker logs --since 1h quizapp_web

# Show logs from a specific time:
docker logs --since "2026-07-11T00:00:00" quizapp_web


# ─────────────────────────────────────────────────────────────
# 6. STOP THE CONTAINER
# ─────────────────────────────────────────────────────────────
#
# Purpose:
#   Gracefully shuts down the Flask application and stops
#   the container. The container transitions from "Up" to
#   "Exited" status.
#
# How it works:
#   1. Docker sends SIGTERM to the main process (python app.py)
#   2. Flask has up to 10 seconds to finish pending requests
#      and close the database connection cleanly
#   3. If the process doesn't exit within the timeout, Docker
#      sends SIGKILL to force-terminate
#
# What is preserved:
#   ✅ Named volume (quiz_data) — database is safe
#   ✅ Container filesystem — can be restarted
#   ✅ Container configuration — port mappings, env vars
#
# What is NOT deleted:
#   The container still exists in "Exited" state. Use
#   "docker rm" to fully remove it.

docker stop quizapp_web

# Custom grace period (30 seconds for slow shutdown):
docker stop -t 30 quizapp_web

# Restart a stopped container (without creating a new one):
docker start quizapp_web


# ─────────────────────────────────────────────────────────────
# 7. REMOVE THE CONTAINER
# ─────────────────────────────────────────────────────────────
#
# Purpose:
#   Permanently deletes the container. This frees the container
#   name ("quizapp_web") so you can create a new one.
#
# ⚠️ Important:
#   • The container must be stopped first (or use -f)
#   • The named volume (quiz_data) is NOT deleted
#   • Your database is safe
#   • The image is NOT deleted — you can create new containers
#
# When to use:
#   • Before re-running "docker run" with the same --name
#   • After testing to clean up
#   • When changing run configuration (ports, volumes, etc.)

docker rm quizapp_web

# Force-remove a running container (stop + remove in one step):
docker rm -f quizapp_web

# Remove all stopped containers at once:
docker container prune


# ─────────────────────────────────────────────────────────────
# 8. INTERACT WITH A RUNNING CONTAINER
# ─────────────────────────────────────────────────────────────
#
# Purpose:
#   Opens a shell session inside the running container,
#   letting you inspect files, check configurations, or
#   debug issues in real-time.
#
# Flags explained:
#   -i  →  Interactive: keeps stdin open for typing commands
#   -t  →  Terminal: allocates a pseudo-TTY for a proper shell

# Open an interactive bash shell:
docker exec -it quizapp_web /bin/bash

# Run a single command without entering the shell:
docker exec quizapp_web whoami
# → appuser (confirms non-root execution)

docker exec quizapp_web python -c "print('Hello from container!')"

# Check the database file exists:
docker exec quizapp_web ls -la /app/instance/

# Check installed Python packages:
docker exec quizapp_web pip list


# ─────────────────────────────────────────────────────────────
# 9. INSPECT CONTAINER & IMAGE DETAILS
# ─────────────────────────────────────────────────────────────
#
# Purpose:
#   Returns the complete configuration of a container or
#   image in JSON format — useful for debugging networking,
#   volume mounts, environment variables, and health status.

# Full container details (JSON):
docker inspect quizapp_web

# Health check status only:
docker inspect --format='{{.State.Health.Status}}' quizapp_web
# → healthy

# Container IP address:
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' quizapp_web

# Environment variables set in the container:
docker inspect --format='{{range .Config.Env}}{{println .}}{{end}}' quizapp_web

# Live CPU/memory/network usage:
docker stats quizapp_web

# Continuous monitoring (press Ctrl+C to exit):
docker stats --no-stream quizapp_web


# ─────────────────────────────────────────────────────────────
# 10. MANAGE VOLUMES (DATABASE PERSISTENCE)
# ─────────────────────────────────────────────────────────────
#
# Purpose:
#   Named volumes store the SQLite database outside the
#   container filesystem, ensuring data survives container
#   removal and rebuilds.
#
# Volume name: quizapp_sqlite_data (set in docker-compose.yml)
# Mount point: /app/instance inside the container

# List all volumes:
docker volume ls

# Filter to quiz app volumes:
docker volume ls | grep quiz

# Inspect volume details (shows host filesystem path):
docker volume inspect quizapp_sqlite_data

# ⚠️ DANGER: Remove the volume (permanently deletes database):
# docker volume rm quizapp_sqlite_data

# ⚠️ DANGER: Remove ALL unused volumes:
# docker volume prune


# ─────────────────────────────────────────────────────────────
# 11. CLEAN UP DOCKER RESOURCES
# ─────────────────────────────────────────────────────────────
#
# Purpose:
#   Over time, Docker accumulates unused images, stopped
#   containers, and dangling layers. These commands free
#   disk space.

# Remove the application image:
# docker rmi quizapp-pipeline:latest

# Remove all dangling images (untagged, intermediate layers):
docker image prune

# Remove all stopped containers:
docker container prune

# Nuclear option — remove everything unused:
# ⚠️ This removes ALL unused images, containers, networks, and volumes
# docker system prune -a --volumes

# Check Docker disk usage:
docker system df


# ─────────────────────────────────────────────────────────────
# QUICK REFERENCE — FULL LIFECYCLE
# ─────────────────────────────────────────────────────────────
#
# ┌─────────┐     ┌─────────┐     ┌─────────┐
# │  BUILD  │ ──▶ │   RUN   │ ──▶ │  VERIFY │
# └─────────┘     └─────────┘     └─────────┘
#
# Build:
#   docker build -t quizapp-pipeline:latest .
#
# Run:
#   docker run -d --name quizapp_web -p 5000:5000 \
#     -v quiz_data:/app/instance --env-file .env \
#     --restart unless-stopped quizapp-pipeline:latest
#
# Verify:
#   docker ps
#   docker logs -f quizapp_web
#   curl -sI http://localhost:5000
#
# Stop:
#   docker stop quizapp_web
#
# Remove:
#   docker rm quizapp_web
#
# Rebuild (full cycle):
#   docker rm -f quizapp_web
#   docker build -t quizapp-pipeline:latest .
#   docker run -d --name quizapp_web -p 5000:5000 \
#     -v quiz_data:/app/instance --env-file .env \
#     --restart unless-stopped quizapp-pipeline:latest
