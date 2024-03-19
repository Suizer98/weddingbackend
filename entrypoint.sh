#!/bin/bash

# Configuration for PostgreSQL
HOST=db
PORT=5432

# Use environment variables directly
USER=$POSTGRES_USER
PASSWORD=$POSTGRES_PASSWORD
DB=$POSTGRES_DB

# Wait for PostgreSQL to be ready
echo "Checking PostgreSQL readiness..."
until PGPASSWORD=$PASSWORD psql -h "$HOST" -U "$USER" -d "$DB" -p "$PORT" -c '\q'; do
  >&2 echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done

>&2 echo "PostgreSQL is up - executing command"
exec "$@"
