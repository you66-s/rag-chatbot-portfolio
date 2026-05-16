#!/bin/bash
set -e

DB_HOSTNAME="${DB_HOSTNAME:-mysql}"
DB_PORT="${DB_PORT:-3306}"
DB_USER_NAME="${DB_USER_NAME:-root}"
DB_PASSWORD="${DB_PASSWORD:-}"

echo "Waiting for MySQL at ${DB_HOSTNAME}:${DB_PORT}..."
python - <<'PY'
import os, time
import pymysql
host = os.getenv('DB_HOSTNAME', 'mysql')
port = int(os.getenv('DB_PORT', '3306'))
user = os.getenv('DB_USER_NAME', 'root')
password = os.getenv('DB_PASSWORD', '')
while True:
    try:
        conn = pymysql.connect(host=host, port=port, user=user, password=password, connect_timeout=5)
        conn.close()
        print(f"MySQL is available at {host}:{port}")
        break
    except Exception as exc:
        print(f"MySQL unavailable, retrying in 2s: {exc}")
        time.sleep(2)
PY

echo "Running database migrations..."
cd /app/
alembic upgrade head

echo "Starting application..."
exec "$@"