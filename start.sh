#!/bin/sh
# Bootstrap a local academic environment without exposing credentials.
set -eu
cd "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
if ! command -v docker >/dev/null 2>&1; then
    echo "Docker with Compose is required. Start Docker Desktop and retry." >&2
    exit 1
fi
docker compose version >/dev/null
docker info >/dev/null 2>&1 || {
    echo "Docker engine is not running. Start it and retry." >&2
    exit 1
}
if [ ! -f .env ]; then
    umask 077
    temporary=$(mktemp .env.XXXXXX)
    trap 'rm -f "$temporary"' 0 1 2 15
    docker run --rm -i python:3.12-slim python - < scripts/create_env.py > "$temporary"
    test -s "$temporary"
    chmod 600 "$temporary"
    mv "$temporary" .env
fi
chmod 600 .env
docker compose up --build --wait --wait-timeout 180
port="${WEB_PORT:-$(sed -n 's/^WEB_PORT=//p' .env | head -1)}"
echo "Application is healthy. Open http://localhost:$port/"
echo "Admin: /admin/ . Local credentials: DEMO_ADMIN_USER and DEMO_ADMIN_PASSWORD in .env."
echo "Never share .env, credentials or database volumes. This is an academic local environment."
