#!/usr/bin/env bash
set -o errexit  # exit on any error

# Define default arguments
MODE=$1

# Build steps (run once on deploy)
if [ "$MODE" = "build" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt

    echo "Running makemigrations and migrate..."
    python manage.py makemigrations --noinput
    python manage.py migrate --noinput

    echo "Collecting static files..."
    python manage.py collectstatic --noinput

# 👑 Create a default admin user if it doesn't exist
echo "👑 Creating default superuser if not exists..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
username = "dan"
email = "olorunfemidaniel53@gmail.com"
password = "2004"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print("✅ Superuser created: username='admin' | password='admin1234'")
else:
    print("ℹ️ Superuser already exists.")
EOF

    exit 0
fi

# Start server
if [ "$MODE" = "start" ]; then
    echo "Starting Django Gunicorn server..."
    gunicorn finance.wsgi:application --bind 0.0.0.0:$PORT
fi
