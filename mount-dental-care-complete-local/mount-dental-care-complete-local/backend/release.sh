#!/usr/bin/env bash
# Release step: runs against the real database before the new version takes
# over. Safe to run on every deploy — every step is idempotent.
set -o errexit

python manage.py migrate --noinput

# Publish the bundled default content (site settings, services, doctors,
# gallery, awards, nav, editable text blocks...) and copy seed_media into
# MEDIA_ROOT. Existing records are only filled where they are blank, so
# anything edited in Django Admin is preserved. Set SEED_RESET=true for the
# very first deploy if you want the bundled copy to win over leftovers.
if [ "${SEED_ON_DEPLOY:-true}" = "true" ]; then
  if [ "${SEED_RESET:-false}" = "true" ]; then
    python manage.py seed_demo --reset
  else
    python manage.py seed_demo
  fi
fi

# Admin account for the deployed site (DJANGO_SUPERUSER_USERNAME/PASSWORD).
python manage.py ensure_admin
