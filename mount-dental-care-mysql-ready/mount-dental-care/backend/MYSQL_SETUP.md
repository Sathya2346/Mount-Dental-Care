# MySQL Setup – Mount Dental Care

## Local XAMPP
1. Start MySQL in XAMPP.
2. Create a database named `mount_dental_care` using utf8mb4.
3. Copy `.env.example` to `.env` and set `MYSQL_PASSWORD` if your root user has one.
4. Create/activate a Python virtual environment and install requirements:
   `pip install -r requirements.txt`
5. Run:
   `python manage.py check`
   `python manage.py migrate`
   `python manage.py seed_demo`
   `python manage.py ensure_admin`
6. Start the backend with `python manage.py runserver`.

## Deployment
Set the following environment variables in the host: `USE_MYSQL=true`, `MYSQL_DATABASE`,
`MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST`, and `MYSQL_PORT=3306`. Alternatively use
a MySQL `DATABASE_URL` supported by `dj-database-url`. Run `migrate`, `seed_demo`,
`ensure_admin`, and `collectstatic` during release/deploy. Keep `MEDIA_ROOT_DIR` on a
persistent disk because MySQL does not store uploaded media files.

## Important
- `seed_demo` is idempotent and creates the bundled CMS data; it does not migrate old
  SQLite user/appointment rows automatically. Export/import those separately if needed.
- Do not commit real passwords, Gmail app passwords, or Django secret keys.
