# The Nigerian Entrepreneur — Django site

The designs supplied as screenshots are implemented as a **Django project**
rendering the original hand-built HTML / CSS / JavaScript. The static assets
(`assets/`) are served through Django's `{% static %}` tag and every page is a
template extending one shared base layout.

## Run it

```bash
pip install -r requirements.txt
python manage.py migrate        # creates db.sqlite3 (admin/sessions only)
python manage.py runserver      # http://127.0.0.1:8000/
```

Environment variables (all optional, sensible dev defaults):

| Variable                     | Default                           |
| ---------------------------- | --------------------------------- |
| `DJANGO_SECRET_KEY`          | dev-only insecure key             |
| `DJANGO_DEBUG`               | `1` (`0` when `RENDER` is set)    |
| `DJANGO_ALLOWED_HOSTS`       | `localhost,127.0.0.1`             |
| `DJANGO_CSRF_TRUSTED_ORIGINS`| — (Render domain appended)        |
| `DATABASE_URL`               | — (SQLite when unset)             |
| `MEDIA_ROOT`                 | `<repo>/media`                    |
| `DJANGO_SUPERUSER_USERNAME` / `_PASSWORD` / `_EMAIL` | — (bootstrap)  |

## Deploy to Render

The repo ships a [`render.yaml`](render.yaml) blueprint — in Render choose
**New → Blueprint → this repo** and it provisions everything:

- **Web service** (Python, gunicorn) + **Postgres** database;
- build = `pip install → collectstatic → migrate → bootstrap_site`;
- `bootstrap_site` seeds an empty database (editorial library, **15 posts per
  category filter chip**) and creates a superuser when `DJANGO_SUPERUSER_*`
  is set in the service environment;
- static files are served by **WhiteNoise** (Render has no web server);
- production defaults kick in automatically when `RENDER` is set:
  `DEBUG=0`, `RENDER_EXTERNAL_HOSTNAME` added to `ALLOWED_HOSTS` and
  `CSRF_TRUSTED_ORIGINS`, HTTPS-aware cookies via the proxy header.

Notes:

- **Uploads** land in `media/`, which is ephemeral on Render. To keep cover
  uploads across deploys, attach a **Persistent Disk** and set
  `MEDIA_ROOT=/opt/render/project/src/media`; otherwise prefer cover **URLs**
  for production posts.
- The seeded fallback admin is `admin` / `naija-admin-2025` — set
  `DJANGO_SUPERUSER_USERNAME` + `DJANGO_SUPERUSER_PASSWORD` to override
  (re-applied on every deploy).
- `PYTHON_VERSION` is pinned in `render.yaml` (3.14.5); bump it if Render
  lists a newer patch release.
- Push to GitHub first — Render deploys from git, so everything must be
  committed (including currently untracked files such as
  `core/context_processors.py`, `core/management/commands/*.py` added lately
  and `core/migrations/0003_*.py`).

## Layout

```
manage.py                        Django entry point
config/                          settings, urls, wsgi/asgi
core/                            the site app
  content.py                     page content (categories, cards, CTA bands)
  views.py                       home / category / page / article / 404
  urls.py                        "/", "category/<slug>/", "article/<slug>/", "<slug>/"
templates/
  base.html                      <head>, header nav, footer, scripts + blocks
  includes/feature_card.html     spotlight article card
  includes/mini_card.html        small article card (with load-more variant)
  pages/home.html                Homepage
  pages/category.html            shared by all 5 category archives
  pages/{services,about,contact,privacy_policy,article,404}.html
assets/                          served as {% static 'css/style.css' %} etc.
  css/style.css                  single stylesheet (tokens + components)
  js/main.js                     all behaviour, vanilla JS
  img/*.svg, img/photos/*.jpg    illustrations / photos
tools/                           helpers (see below)
reference/                       the 7 original design screenshots
```

### Templates

- `templates/base.html` holds the shared shell. Child pages override
  `{% block title %}`, `{% block meta_description %}`, `{% block page_id %}`
  (drives `<body data-page="…">`) and `{% block content %}`; optional
  `{% block extra_head %}` / `{% block scripts %}` are also available.
- The header marks the active nav entry via the `nav_active` context variable
  (`finance`, `business`, `crypto`, `entrepreneur`, `affiliate`, `more`).
- The five category archives (finance, business, crypto, entrepreneur,
  affiliates) all render `pages/category.html` from data in
  `core/content.py` — edit that file to change heroes, chips, cards or CTA
  bands. Card hrefs use `"url-name:arg"` (resolved with `reverse()`) or
  literals like `"#latest"`.
- Static pages and the article page live under `templates/pages/` and are
  mapped in `core/content.py` (`STATIC_PAGES`, `ARTICLES`).

## Behaviour (assets/js/main.js)

- Sticky header with hover dropdowns on desktop, accordion drawer on mobile
- Search panel drawer (`#searchToggle`)
- Category filter chips — filters the article list by tag, with an empty state
- "Load more articles" — reveals the remaining hidden entries, then removes itself
- Newsletter + contact form validation with inline status messages and a toast
- `data-copy-link` copy-link button, scroll-spy for the privacy/article TOCs
- IntersectionObserver reveal animations with a safety net so content is never
  left hidden, plus `prefers-reduced-motion` and print fallbacks
- Back-to-top button, auto footer year

## Tools

- `tools/extract_django_templates.py` — one-off bootstrap that generated
  `templates/base.html` and the page templates from the legacy flat HTML
  files (kept for traceability; safe to re-run, it overwrites its outputs).
- `tools/verify_django_pages.py` — renders every route with the test client
  and fails on template errors, leftover `assets/…` links or missing static
  URLs. Run it after template changes: `python tools/verify_django_pages.py`
- `tools/spotcheck_category.py` — structure spot-check for the shared
  category template (cards, chips, load-more, CTA).
- `tools/build.mjs` + `tools/content-*.mjs` — the legacy Node static-site
  generator that produced the flat `*.html` files still at the repo root.
  Those files are kept for reference; the Django templates are now the
  source of truth.
