import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
os.environ.setdefault("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,testserver")
# DEBUG=0 so the custom handler404 (pages/404.html) is exercised, as in production.
os.environ.setdefault("DJANGO_DEBUG", "0")

import django

django.setup()

from django.test import Client

from core.models import Post

client = Client()

PUBLIC_ROUTES = [
    "/",
    "/services/",
    "/about/",
    "/contact/",
    "/privacy-policy/",
    "/category/finance/",
    "/category/business/",
    "/category/crypto/",
    "/category/entrepreneur/",
    "/category/affiliates/",
    "/article/10-profitable-business-ideas/",
    "/signup/",
    "/login/",
    "/tools/currency/",
    "/markets/",
]

# Dynamic blog-detail route from seeded data.
first_post = Post.published().first()
if first_post:
    PUBLIC_ROUTES.append(f"/blog/{first_post.slug}/")

failures = []


def check(route, expect=200, label=None):
    label = label or route
    resp = client.get(route)
    body = resp.content.decode("utf-8", errors="replace")
    problems = []
    if resp.status_code != expect:
        problems.append(f"status={resp.status_code} (expect {expect})")
    if resp.status_code == 200:
        if "{%" in body or "{{" in body:
            problems.append("unrendered template syntax")
        if "css/style.css" not in body:
            problems.append("stylesheet link missing")
        if "/static/" not in body:
            problems.append("no /static/ URLs rendered")
    if problems:
        failures.append((route, problems))
        print(f"{resp.status_code}  {label}  {'; '.join(problems)}")
    else:
        print(f"{resp.status_code}  {label}  OK")


print("== Public pages ==")
for route in PUBLIC_ROUTES:
    check(route)

print("\n== 404 handler ==")
resp = client.get("/does-not-exist/")
print(f"{resp.status_code}  /does-not-exist/  (expect 404)  "
      + ("OK" if resp.status_code == 404 else "FAIL"))
if resp.status_code != 404:
    failures.append(("/does-not-exist/", ["did not return 404"]))
body = resp.content.decode("utf-8", errors="replace")
if "Page Not Found" not in body:
    failures.append(("/does-not-exist/", ["404 template not rendered"]))

print("\n== Active-nav spot check ==")
resp = client.get("/category/finance/")
body = resp.content.decode("utf-8", errors="replace")
if "nav__item has-menu is-active" not in body:
    failures.append(("/category/finance/", ["nav active mark missing"]))
    print("nav active mark missing on /category/finance/")
else:
    print("nav active mark OK on /category/finance/")

print("\n== Authenticated dashboards ==")
assert client.login(username="admin", password="naija-admin-2025"), "admin login failed"
for route in ["/panel/", "/panel/posts/", "/panel/comments/"]:
    check(route, label=f"[admin] {route}")
assert client.login(username="ngozi", password="naija-creator-2025"), "ngozi login failed"
check("/dashboard/", label="[creator] /dashboard/")

print()
if failures:
    print("FAILURES:")
    for route, problems in failures:
        print(f"  {route}: {problems}")
    raise SystemExit(1)
print("ALL ROUTES OK")
