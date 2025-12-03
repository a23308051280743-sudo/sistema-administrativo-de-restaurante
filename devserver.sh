#!/bin/sh
source .venv/bin/activate
python backend_restaurant/manage.py runserver 0.0.0.0:${PORT:-8001}
