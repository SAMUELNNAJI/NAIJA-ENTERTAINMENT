"""End-to-end smoke test for AJAX comment create/edit/delete."""
import django, os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
os.environ.setdefault("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,testserver")
django.setup()

from django.test import Client
from core.models import Post, Comment

c = Client()
post = Post.published().first()
assert post, "No published post; run manage.py seed first"
slug = post.slug

# Log in as staff so edit/delete (staff override) are allowed.
assert c.login(username="admin", password="naija-admin-2025"), "admin login failed"

# CREATE
r = c.post(
    f"/blog/{slug}/comment/",
    {"name": "AJAX Tester", "email": "ajax@example.com", "body": "Hello via AJAX"},
    HTTP_X_REQUESTED_WITH="XMLHttpRequest",
)
assert r.status_code == 200, r.content
body = r.json()
assert body["ok"] is True, body
cid = body["comment"]["id"]
print("CREATE OK -> comment id", cid)

# EDIT
r = c.post(
    f"/comment/{cid}/edit/",
    {"name": "AJAX Tester", "email": "ajax@example.com", "body": "Edited via AJAX"},
    HTTP_X_REQUESTED_WITH="XMLHttpRequest",
)
assert r.status_code == 200, r.content
assert r.json()["ok"] is True, r.json()
print("EDIT OK")

# Confirm the edit persisted in DB
comment = Comment.objects.get(pk=cid)
assert comment.body == "Edited via AJAX", comment.body
print("DB edit persisted OK")

# DELETE
r = c.post(
    f"/comment/{cid}/delete/", {}, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
)
assert r.status_code == 200, r.content
assert r.json()["ok"] is True, r.json()
assert not Comment.objects.filter(pk=cid).exists()
print("DELETE OK")
print("AJAX COMMENT FLOW: ALL PASS")
