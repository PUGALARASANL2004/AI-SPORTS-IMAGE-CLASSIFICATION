#!/usr/bin/env bash
# Exit on error
set -o errexit

# Upgrade build tools
pip install --upgrade pip setuptools wheel

# Install dependencies
pip install -r requirements.txt

# Convert static files
python manage.py collectstatic --no-input

# Apply migrations
python manage.py migrate
