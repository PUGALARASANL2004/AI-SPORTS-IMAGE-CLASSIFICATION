#!/usr/bin/env bash
# Exit on error
set -o errexit

# Upgrade build tools to ensure we can install modern packages
pip install --upgrade pip setuptools wheel

# Install dependencies needed for building some packages
pip install --upgrade "setuptools>=70.0.0" "wheel>=0.40.0"

# Install dependencies
pip install -r requirements.txt

# Convert static files
python manage.py collectstatic --no-input

# Apply migrations
python manage.py migrate
