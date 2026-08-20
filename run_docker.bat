@echo off
echo ==============================================
echo   Starting BrainCheck Quiz App (Docker)
echo ==============================================

echo Building and starting the containers in detached mode...
docker compose up -d --build

echo.
echo BrainCheck is starting! You can access it at http://localhost:5000
echo To view logs, use: docker compose logs -f
echo To stop, use: docker compose down
echo.
pause
