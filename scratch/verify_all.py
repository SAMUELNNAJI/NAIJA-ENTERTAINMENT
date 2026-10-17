import os
import sys
import django

sys.path.insert(0, os.path.abspath("."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.conf import settings
if "testserver" not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS.append("testserver")

from django.test import Client
from django.contrib.auth.models import User
from core.models import Post, CreatorProfile, SponsorAd
from core.forms import PostForm, SponsorAdForm

print("1. Running Django checks...")
from django.core.management import call_command
call_command("check")
print("Django check passed!")

# Create or get a staff user
staff_user, _ = User.objects.get_or_create(username="test_staff", defaults={"email": "staff@example.com", "is_staff": True, "is_superuser": True})
staff_user.is_staff = True
staff_user.save()

client = Client()
client.force_login(staff_user)

print("\n2. Testing Switch to Creator for Staff...")
# When accessing with ?view=creator
resp = client.get("/dashboard/?view=creator")
print(f"GET /dashboard/?view=creator: status {resp.status_code}")
assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
assert client.session.get("dashboard_view") == "creator", "Session dashboard_view should be creator"
content_str = resp.content.decode("utf-8")
assert "Total Amount Earned" in content_str, "Total Amount Earned should be rendered in Creator Studio"
assert "Creator Studio" in content_str, "Creator Studio should be rendered"
print("Creator Studio loaded with Total Amount Earned rendered!")

# When accessing stories or new post as creator
resp_new = client.get("/dashboard/post/new/")
print(f"GET /dashboard/post/new/: status {resp_new.status_code}")
assert resp_new.status_code == 200, f"Expected 200, got {resp_new.status_code}"
content_new = resp_new.content.decode("utf-8")
assert "dashboard-editor" in content_new, "Editor styles container should be present"

# Switch to Admin
resp_admin = client.get("/panel/?view=admin")
print(f"GET /panel/?view=admin: status {resp_admin.status_code}")
assert resp_admin.status_code == 200, f"Expected 200, got {resp_admin.status_code}"
assert client.session.get("dashboard_view") == "admin", "Session dashboard_view should be admin"
content_admin = resp_admin.content.decode("utf-8")
assert "Total Amount Earned" in content_admin, "Total Amount Earned should be rendered in Admin"
assert "Command Center" in content_admin, "Command Center should be rendered"
print("Admin Panel loaded with Total Amount Earned rendered!")

# Check Admin New Post
resp_admin_new = client.get("/panel/posts/new/")
print(f"GET /panel/posts/new/: status {resp_admin_new.status_code}")
assert resp_admin_new.status_code == 200, f"Expected 200, got {resp_admin_new.status_code}"
assert "dashboard-editor" in resp_admin_new.content.decode("utf-8")

print("\n3. Testing Password Reset views...")
resp_pr = client.get("/password-reset/")
print(f"GET /password-reset/: status {resp_pr.status_code}")
assert resp_pr.status_code == 200

resp_prd = client.get("/password-reset/done/")
print(f"GET /password-reset/done/: status {resp_prd.status_code}")
assert resp_prd.status_code == 200

resp_prc = client.get("/password-reset-complete/")
print(f"GET /password-reset-complete/: status {resp_prc.status_code}")
assert resp_prc.status_code == 200

print("\n4. Testing Error templates rendering...")
from django.template.loader import render_to_string
t400 = render_to_string("400.html", {})
assert "400" in t400 and "Bad Request" in t400
t403 = render_to_string("403.html", {})
assert "403" in t403 and "Access Restricted" in t403
t404 = render_to_string("404.html", {})
assert "404" in t404 and "Lost in the Ecosystem" in t404
t500 = render_to_string("500.html", {})
assert "500" in t500 and "Server Anomaly" in t500
print("All 4 error templates render successfully!")

print("\n5. Testing Image Upload on Forms...")
post_form = PostForm()
assert "cover_upload" in post_form.fields, "PostForm must have cover_upload"
assert "image_url" in post_form.fields, "PostForm must have image_url"

sponsor_form = SponsorAdForm()
assert "cover_upload" in sponsor_form.fields, "SponsorAdForm must have cover_upload"
assert "image_url" in sponsor_form.fields, "SponsorAdForm must have image_url"
print("PostForm and SponsorAdForm both have image URL and image file upload!")

print("\n=== ALL VERIFICATIONS PASSED SUCCESSFULLY! ===")
