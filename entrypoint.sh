#!/bin/sh

echo "Waiting for PostgreSQL..."
./wait-for-postgres.sh

echo "Running database seed..."
python seed.py

echo "Starting Flask server..."
flask run --host=0.0.0.0 --port=5000
