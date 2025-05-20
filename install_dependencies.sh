#!/bin/bash

# Exit on error
set -e

echo "=== Checking Python version ==="
python --version

echo "=== Installing system dependencies ==="
sudo apt-get update
sudo apt-get install -y build-essential libssl-dev libbz2-dev libffi-dev

echo "=== Removing existing lock file ==="
rm -f poetry.lock

echo "=== Configuring Poetry to use pre-built wheels when possible ==="
poetry config experimental.new-installer false
poetry config installer.parallel false

echo "=== Running Poetry lock ==="
poetry lock --no-update

echo "=== Installing dependencies with Poetry ==="
# Use --no-dev to skip development dependencies if installation fails
poetry install --no-interaction --no-build-isolation || poetry install --no-dev --no-interaction --no-build-isolation

echo "=== Installation complete ==="
echo "You can now activate the virtual environment with: poetry shell" 