#!/bin/bash
set -e

echo "🔨 Building SavFi-Backend for Render..."

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

echo "✅ Build complete!"
