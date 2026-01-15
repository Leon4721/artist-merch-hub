#!/usr/bin/env bash

# 1. Install dependencies from requirements.txt
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# 2. Run collectstatic
echo "📦 Running collectstatic..."
python manage.py collectstatic --noinput

# 3. Run migrations
echo "🛠 Running migrations..."
python manage.py migrate --noinput
