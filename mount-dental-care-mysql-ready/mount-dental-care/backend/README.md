# Django Backend

Needs Python 3.12 (and Node 22 only if you want to build the React app here).

**Database:** local development uses SQLite (`backend/db.sqlite3`) with no
configuration at all. A deployment sets `DATABASE_URL` to a PostgreSQL
connection string and the same settings file switches over. The host also
serves the built React app, so one service runs the whole site — see
[DEPLOY.md](../DEPLOY.md) for the full deployment and verification guide.

## 1. Setup Python

```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in the Gmail details (and the deployment
values if you are deploying). If you do not use python-dotenv, export the same
variables in your terminal.

## 3. Migrate + create admin

```bash
python manage.py migrate
python manage.py createsuperuser     # or: python manage.py ensure_admin
```

## 4. Seed the screenshot content

```bash
python manage.py seed_demo
```

Then open `http://127.0.0.1:8000/admin/`.

## 5. Run backend

```bash
python manage.py runserver
```

During development the React app (started with `npm run dev`) calls the API at
`http://127.0.0.1:8000/api` automatically. When Django serves the built app
itself, the frontend uses `/api` on the same origin — no CORS setup needed.

## 6. Checks

```bash
python manage.py test clinic         # admin CRUD + seeded content + API contract
python manage.py check --deploy      # production configuration warnings
```

## CMS behavior

- Admin can edit all website text/content.
- Admin can upload/replace logo, hero images, doctor images, gallery images and gallery videos.
- Admin can view all appointment submissions.
- Admin can change appointment status and add an admin note.
- Status changes create a notification automatically. Registered patients get it on their account; guest bookings keep it against their email address and claim it when they register with that address.
- Admin can create custom notifications from the Notification admin screen.
- Registered users can see their appointments and notifications in the User Panel.
