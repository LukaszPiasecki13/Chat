#!/bin/bash
python manage.py migrate
python manage.py seed
daphne -b 0.0.0.0 -p 8000 core.asgi:application

