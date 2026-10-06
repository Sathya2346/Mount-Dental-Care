#!/usr/bin/env bash
# Build step for the host (Render/Railway/Heroku/DigitalOcean App Platform...).
# Run from the backend/ directory — it also builds the React app, because the
# Django app serves frontend/dist itself (see config/urls.py: serve_react).
set -o errexit

python -m pip install --upgrade pip
pip install -r requirements.txt

# --- React frontend -------------------------------------------------------
# VITE_API_BASE is left unset on purpose: src/api.js then falls back to the
# same-origin "/api", so the bundle talks to whatever domain serves it and no
# CORS configuration is needed.
if [ -d ../frontend ]; then
  cd ../frontend
  if [ -f package-lock.json ]; then npm ci; else npm install; fi
  npm run build
  cd ../backend
fi

python manage.py collectstatic --noinput
