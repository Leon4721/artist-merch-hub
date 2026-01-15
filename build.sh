#!/usr/bin/env bash
# build.sh - for Render.com

echo "📦 Running collectstatic..."
python manage.py collectstatic --noinput

echo "🛠 Running migrations..."
python manage.py migrate --noinput
