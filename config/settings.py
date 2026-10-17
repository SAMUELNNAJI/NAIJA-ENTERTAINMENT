"""
Django settings for "The Nigerian Entrepreneur" site.

The project reuses the existing static front end:

  - assets/  -> STATICFILES_DIRS, so {% static 'css/style.css' %} resolves to
                assets/css/style.css (no files were moved)
  - templates/ -> TEMPLATES DIRS, one base.html + one template per page
"""
from pathlib import Path
import os

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env (git-ignored) into the environment. Real environment variables
# always win over .env values; falls back gracefully if python-dotenv is
# not installed.
try:
    from dotenv import load_dotenv

    load_dotenv(BASE_DIR / ".env")
except ImportError:
    pass

# Render sets RENDER=true and RENDER_EXTERNAL_HOSTNAME on every service, so
# safe production defaults apply automatically without code edits.
ON_RENDER = os.environ.get("RENDER", "").lower() in ("1", "true", "yes")

# Set DJANGO_SECRET_KEY in production; the fallback is dev-only. On Render,
# render.yaml generates one automatically (`generateValue: true`).
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")
if not SECRET_KEY:
    if ON_RENDER:
        raise ImproperlyConfigured(
            "DJANGO_SECRET_KEY is not set. render.yaml generates one "
            "(generateValue) — set it in the service Environment panel."
        )
    SECRET_KEY = "django-insecure-dev-only-do-not-use-in-production"

# Set DJANGO_DEBUG=0 for production. Defaults to ON locally, OFF on Render.
DEBUG = os.environ.get("DJANGO_DEBUG", "0" if ON_RENDER else "1") == "1"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")
    if host.strip()
] or ["localhost", "127.0.0.1"]
# Always allow the Render service's own domain (*.onrender.com).
if os.environ.get("RENDER_EXTERNAL_HOSTNAME"):
    ALLOWED_HOSTS.append(os.environ["RENDER_EXTERNAL_HOSTNAME"])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise serves collectstatic output — Render has no web server of
    # its own, so static files must come from the Django process.
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.active_sponsor_ads",
            ],
            "builtins": ["core.templatetags.tne_tags"],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Render injects DATABASE_URL (Postgres) for the linked database; local
# development falls back to SQLite.
DATABASE_URL = os.environ.get("DATABASE_URL", "")
if DATABASE_URL:
    import dj_database_url

    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL, conn_max_age=600, conn_health_checks=True
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = []

# The static site's assets/ directory — served at {% static '...' %}.
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "assets"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise serves collectstatic output in production; the manifest
# storage fingerprints files for long-lived browser caching.
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Uploaded covers (dashboard "Cover image upload") — served in dev via
# django.conf.urls.static. On Render, attach a persistent disk and point
# MEDIA_ROOT at it (e.g. /opt/render/project/src/media) so uploads survive
# redeploys; without a disk, prefer cover URLs for production posts.
MEDIA_URL = "/media/"
MEDIA_ROOT = Path(os.environ.get("MEDIA_ROOT", str(BASE_DIR / "media")))

# --- production hardening (applied whenever DEBUG is off) ---
# Render terminates TLS at its edge proxy and forwards the scheme via
# X-Forwarded-Proto; Django needs that to treat requests as HTTPS.
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
if ON_RENDER:
    # The Render edge forces HTTPS for every request, so advertise HSTS.
    SECURE_HSTS_SECONDS = 60 * 60 * 24 * 365
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False

# HTTP→HTTPS is handled at the Render edge (and SECURE_SSL_REDIRECT would
# break its http:// health checks), so the Django-level redirect is skipped.
SILENCED_SYSTEM_CHECKS = ["security.W008"]

# POSTs (login, comments, subscribe) from the Render domain need an
# explicit origin allow-list (required since Django 4).
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]
if os.environ.get("RENDER_EXTERNAL_HOSTNAME"):
    CSRF_TRUSTED_ORIGINS.append(f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Auth redirects
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "home"

# Email Configuration for Password Reset & Notifications
EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend" if DEBUG else "django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.sendgrid.net")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True").lower() in ("true", "1", "yes")
DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL", "The Nigerian Entrepreneur <noreply@thenigerianentrepreneur.com>"
)
