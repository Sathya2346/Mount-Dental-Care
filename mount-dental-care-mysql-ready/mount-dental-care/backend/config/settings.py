from pathlib import Path
import hashlib
import os
from dotenv import load_dotenv
BASE_DIR=Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent
FRONTEND_DIST = PROJECT_ROOT / "frontend" / "dist"
load_dotenv(BASE_DIR / ".env")
SECRET_KEY=os.getenv('SECRET_KEY','django-insecure-mount-dental-care-dev-key').strip()
# JWT signing (HS256) needs at least 32 bytes of key material. Short dev keys
# trigger an InsecureKeyLengthWarning and produce weak signatures, so stretch
# anything shorter into a stable 64-character key instead of failing.
if len(SECRET_KEY) < 32:
    SECRET_KEY=hashlib.sha256(SECRET_KEY.encode('utf-8')).hexdigest()
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv("ALLOWED_HOSTS", "").split(",")
    if host.strip()
]
INSTALLED_APPS=[
 'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles',
 'corsheaders','rest_framework','rest_framework_simplejwt','clinic',
]
MIDDLEWARE=['corsheaders.middleware.CorsMiddleware','django.middleware.security.SecurityMiddleware','whitenoise.middleware.WhiteNoiseMiddleware','django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware']
ROOT_URLCONF='config.urls'
TEMPLATES=[{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[],'APP_DIRS':True,'OPTIONS':{'context_processors':['django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION='config.wsgi.application'
# Database configuration
# Priority: DATABASE_URL (deployment platforms) -> MYSQL_* variables (local
# XAMPP or a VPS) -> SQLite fallback for backwards compatibility.
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
MYSQL_NAME = os.getenv("MYSQL_DATABASE", "mount_dental_care").strip()
MYSQL_USER = os.getenv("MYSQL_USER", "root").strip()
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1").strip()
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306").strip()

if DATABASE_URL:
    import dj_database_url
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=os.getenv("DB_SSL", "false").lower() == "true",
        )
    }
elif os.getenv("USE_MYSQL", "true").lower() == "true":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": MYSQL_NAME,
            "USER": MYSQL_USER,
            "PASSWORD": MYSQL_PASSWORD,
            "HOST": MYSQL_HOST,
            "PORT": MYSQL_PORT,
            "OPTIONS": {
                "charset": "utf8mb4",
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            },
            "CONN_MAX_AGE": 600,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
AUTH_PASSWORD_VALIDATORS=[]
LANGUAGE_CODE='en-us'; TIME_ZONE='Asia/Kolkata'; USE_I18N=True; USE_TZ=True
# Display all dates as dd/mm/yyyy throughout admin and templates
USE_L10N = False
DATE_FORMAT = 'd/m/Y'
DATETIME_FORMAT = 'd/m/Y, P'
SHORT_DATE_FORMAT = 'd/m/Y'
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise serves the collected static files from the app process, so the
# deployment needs no separate web server or CDN for /static/. Compressed (not
# manifest) storage is deliberate: manifest hashing makes `collectstatic` fail
# whenever a third-party stylesheet points at a file it does not ship.
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
}
WHITENOISE_MAX_AGE = 60 * 60 * 24 * 30
WHITENOISE_KEEP_ONLY_HASHED_FILES = False

MEDIA_URL = "/media/"
# Admin uploads (logo, doctors, gallery, hero banners, awards...) live on the
# app's own filesystem. On a host, set MEDIA_ROOT_DIR to the mounted persistent
# disk so those uploads survive restarts and every deploy.
MEDIA_ROOT = Path(os.getenv("MEDIA_ROOT_DIR") or (BASE_DIR / "media"))
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [
    x.strip()
    for x in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
    if x.strip()
]

# Django 4 requires the full origin (scheme + host) of the deployed site for
# admin logins and any POST coming through the host's proxy.
CSRF_TRUSTED_ORIGINS = [
    x.strip()
    for x in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
    if x.strip()
]

# Hosts terminate TLS at their edge proxy and pass the original scheme in
# X-Forwarded-Proto; without this Django believes every request is plain HTTP
# and redirects the admin in a loop.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
if not DEBUG:
    # Only meaningful over HTTPS, i.e. on the deployed site (DEBUG is off
    # there). Locally DEBUG=True keeps the plain-HTTP dev server working.
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "same-origin"

# Extra HTTPS hardening, off by default because most hosts already redirect
# HTTP -> HTTPS at their proxy. Turn these on (env) once the domain is live and
# HTTPS is confirmed: SECURE_SSL_REDIRECT=true and SECURE_HSTS_SECONDS=31536000.
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "false").lower() == "true"
SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "0"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = SECURE_HSTS_SECONDS > 0
SECURE_HSTS_PRELOAD = SECURE_HSTS_SECONDS > 0
from corsheaders.defaults import default_headers
CORS_ALLOW_HEADERS = list(default_headers) + ['cache-control', 'pragma', 'expires']
REST_FRAMEWORK={'DEFAULT_AUTHENTICATION_CLASSES':['clinic.authentication.OptionalJWTAuthentication'],'DEFAULT_PERMISSION_CLASSES':['rest_framework.permissions.AllowAny']}

EMAIL_BACKEND=os.getenv('EMAIL_BACKEND','django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST=os.getenv('EMAIL_HOST','smtp.gmail.com')
EMAIL_PORT=int(os.getenv('EMAIL_PORT','587'))
EMAIL_USE_TLS=os.getenv('EMAIL_USE_TLS','True').lower()=='true'
EMAIL_HOST_USER=os.getenv('EMAIL_HOST_USER','')
EMAIL_HOST_PASSWORD=os.getenv('EMAIL_HOST_PASSWORD','').replace(' ','').strip()
DEFAULT_FROM_EMAIL=os.getenv('DEFAULT_FROM_EMAIL',EMAIL_HOST_USER)
OTP_EXPIRY_MINUTES=int(os.getenv('OTP_EXPIRY_MINUTES','5'))
# Minimum wait between two verification emails for the same address.
OTP_RESEND_COOLDOWN_SECONDS=int(os.getenv('OTP_RESEND_COOLDOWN_SECONDS','120'))
# Do not let a blocked/unreachable SMTP host hang the booking request forever.
EMAIL_TIMEOUT=int(os.getenv('EMAIL_TIMEOUT','20'))
SERVER_EMAIL=os.getenv('SERVER_EMAIL') or DEFAULT_FROM_EMAIL or 'root@localhost'

# Gunicorn/WhiteNoise log to stdout so the host's log viewer shows requests and
# errors (a silent 500 on the host is otherwise impossible to diagnose).
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {'format': '{levelname} {asctime} {name} {message}', 'style': '{'},
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'simple'},
    },
    'root': {'handlers': ['console'], 'level': os.getenv('LOG_LEVEL', 'INFO')},
    'loggers': {
        'django.request': {'handlers': ['console'], 'level': 'ERROR', 'propagate': False},
    },
}
