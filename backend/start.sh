#!/bin/bash

set -e 

if [ -f /app/db.sqlite3 ]; then
    echo "Deleting old SQLite database..."
    rm /app/db.sqlite3
fi

python manage.py migrate
python manage.py seed
daphne -b 0.0.0.0 -p 8000 core.asgi:application

