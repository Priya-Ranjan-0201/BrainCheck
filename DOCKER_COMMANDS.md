# ============================================================
# Docker Build & Run Instructions
# Dockerized Quiz Application
# ============================================================
#
# This guide covers every Docker CLI command you need to
# build, run, inspect, and manage the Quiz App container.
#
# Prerequisites:
#   • Docker Desktop installed and running
#   • Terminal open in the project root (Dockerized-Quiz-App/)
# ============================================================


# ─────────────────────────────────────────────────────────────
# 1. BUILD THE DOCKER IMAGE
# ─────────────────────────────────────────────────────────────
#
# What it does:
#   Reads the Dockerfile, executes each instruction layer by
#   layer, and produces a tagged image stored locally.
#
#   -t  →  Tags the image with a name:version label
#   .   →  Sets the build context to the current directory
#          (the Dockerfile and .dockerignore must be here)
#
# First build downloads the base image (~50 MB) and installs
# dependencies. Subsequent builds use Docker layer caching and
# finish in seconds if only source code changed.

docker build -t quizapp-pipeline:latest .


# ─────────────────────────────────────────────────────────────
# 2. VERIFY THE IMAGE WAS CREATED
# ─────────────────────────────────────────────────────────────
#
# What it does:
#   Lists all locally stored Docker images. You should see
#   "quizapp-pipeline" with the "latest" tag.
#
#   Useful columns:
#     REPOSITORY   →  Image name
#     TAG          →  Version label
#     SIZE         →  Final compressed size (aim for < 200 MB)

docker images


# ─────────────────────────────────────────────────────────────
# 3. RUN THE CONTAINER
# ─────────────────────────────────────────────────────────────
#
# What it does:
#   Creates and starts a new container from the image.
#
#   -d                →  Detached mode (runs in background)
#   --name            →  Assigns a human-readable container name
#   -p 5000:5000      →  Maps host port 5000 → container port 5000
#   -v quiz_data:/app/instance
#                     →  Mounts a named volume so the SQLite
#                        database persists across restarts
#   --restart unless-stopped
#                     →  Auto-restarts on crash; stays stopped
#                        only when you explicitly stop it
#   --env-file .env   →  Loads all variables from the .env file
#
# After this command, open http://localhost:5000 in your browser.

docker run -d \
  --name quizapp_web \
  -p 5000:5000 \
  -v quiz_data:/app/instance \
  --restart unless-stopped \
  --env-file .env \
  quizapp-pipeline:latest


# ─────────────────────────────────────────────────────────────
# 4. CHECK RUNNING CONTAINERS
# ─────────────────────────────────────────────────────────────
#
# What it does:
#   Shows all currently running containers with their status,
#   port mappings, and uptime.
#
#   -a  →  Also shows stopped containers (optional)
#
#   Look for:
#     STATUS   →  "Up X minutes" means healthy
#     PORTS    →  "0.0.0.0:5000->5000/tcp" confirms the mapping

docker ps

# Include stopped containers:
docker ps -a


# ─────────────────────────────────────────────────────────────
# 5. VIEW CONTAINER LOGS
# ─────────────────────────────────────────────────────────────
#
# What it does:
#   Streams stdout/stderr output from the Flask application.
#   Essential for debugging startup errors, request logs,
#   and database initialisation messages.
#
#   -f          →  Follow (live tail, like "tail -f")
#   --tail 100  →  Show only the last 100 lines
#
# Press Ctrl+C to stop following.

docker logs quizapp_web

# Follow live output:
docker logs -f quizapp_web

# Show last 50 lines only:
docker logs --tail 50 quizapp_web


# ─────────────────────────────────────────────────────────────
# 6. STOP THE CONTAINER
# ─────────────────────────────────────────────────────────────
#
# What it does:
#   Sends SIGTERM to the Flask process, giving it 10 seconds
#   to shut down gracefully. After the timeout, Docker sends
#   SIGKILL to force-stop.
#
#   The container moves to "Exited" status but is NOT deleted.
#   The named volume (quiz_data) and all database data remain.
#
#   -t 10  →  Grace period in seconds (default: 10)

docker stop quizapp_web


# ─────────────────────────────────────────────────────────────
# 7. REMOVE THE CONTAINER
# ─────────────────────────────────────────────────────────────
#
# What it does:
#   Deletes the stopped container. This frees the container
#   name so you can re-use it with "docker run".
#
#   ⚠  The named volume (quiz_data) is NOT deleted.
#      Your database is safe.
#
#   -f  →  Force-remove even if still running (optional)

docker rm quizapp_web

# Force-remove a running container (stop + remove in one step):
docker rm -f quizapp_web


# ─────────────────────────────────────────────────────────────
# BONUS: USEFUL ADDITIONAL COMMANDS
# ─────────────────────────────────────────────────────────────

# Open an interactive shell inside the running container:
docker exec -it quizapp_web /bin/bash

# Inspect full container configuration (JSON):
docker inspect quizapp_web

# Check container resource usage (CPU, memory, network):
docker stats quizapp_web

# List named volumes (verify quiz_data exists):
docker volume ls

# Remove the data volume (⚠ DELETES the database permanently):
# docker volume rm quiz_data

# Remove the image (after removing all containers using it):
# docker rmi quizapp-pipeline:latest

# Prune all unused images, containers, and volumes:
# docker system prune -a --volumes


# ─────────────────────────────────────────────────────────────
# QUICK REFERENCE – FULL LIFECYCLE
# ─────────────────────────────────────────────────────────────
#
#   Build   →  docker build -t quizapp-pipeline:latest .
#   Run     →  docker run -d --name quizapp_web -p 5000:5000 \
#                -v quiz_data:/app/instance --env-file .env \
#                quizapp-pipeline:latest
#   Logs    →  docker logs -f quizapp_web
#   Stop    →  docker stop quizapp_web
#   Remove  →  docker rm quizapp_web
#   Rebuild →  docker build -t quizapp-pipeline:latest . && \
#              docker rm -f quizapp_web && \
#              docker run -d --name quizapp_web -p 5000:5000 \
#                -v quiz_data:/app/instance --env-file .env \
#                quizapp-pipeline:latest
