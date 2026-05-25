#!/bin/sh
set -e

# Start backend in background on internal port 8080
PORT=8080 uv run --no-dev python main.py &
BACKEND_PID=$!

# Substitute environment variables in nginx template
envsubst '$PORT' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

# Cleanup processes on exit
cleanup() {
    kill "$BACKEND_PID" 2>/dev/null || true
    kill "$NGINX_PID" 2>/dev/null || true
    wait "$BACKEND_PID" 2>/dev/null || true
    wait "$NGINX_PID" 2>/dev/null || true
}
trap cleanup INT TERM EXIT

# Start nginx in background (daemon off allows waiting)
nginx -g 'daemon off;' &
NGINX_PID=$!

# Wait for nginx to finish
wait "$NGINX_PID"
