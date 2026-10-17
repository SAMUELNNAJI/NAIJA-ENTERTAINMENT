"""One-shot production bootstrap — the last step of Render's build command.

Idempotent, safe to run on every deploy:

1. On an *empty* database (fresh Render Postgres) it seeds the full
   library: `seed` (base posts, demo accounts, comments) and
   `replace_posts_with_editorial` (original editorial titles). Existing
   content is never touched.
2. Always runs `add_editorial_posts` + `add_chip_posts` — both skip
   existing titles — so new filter-chip entries land as the lists grow.
3. Creates or refreshes a superuser from the standard Django env vars
   (DJANGO_SUPERUSER_USERNAME / _PASSWORD / _EMAIL) when provided.
"""
import os

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand

from core.models import Post


class Command(BaseCommand):
    help = "Seed an empty database and create/refresh the superuser from env."

    def handle(self, *args, **options):
        if not Post.objects.exists():
            self.stdout.write("Empty database — seeding base content...")
            call_command("seed")
            call_command("replace_posts_with_editorial")
        call_command("add_editorial_posts")
        call_command("add_chip_posts")

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "").strip()
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "")
        if username and password:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": os.environ.get("DJANGO_SUPERUSER_EMAIL", ""),
                    "is_superuser": True,
                    "is_staff": True,
                },
            )
            if not created:
                user.is_superuser = True
                user.is_staff = True
                if os.environ.get("DJANGO_SUPERUSER_EMAIL"):
                    user.email = os.environ["DJANGO_SUPERUSER_EMAIL"]
                user.save()
            # The environment is authoritative: (re)set the password each run.
            user.set_password(password)
            user.save(update_fields=["password"])
            verb = "created" if created else "refreshed"
            self.stdout.write(
                self.style.SUCCESS(f"Superuser '{username}' {verb} from env.")
            )
        else:
            self.stdout.write(
                "DJANGO_SUPERUSER_USERNAME/PASSWORD not set — skipping admin."
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Bootstrap complete. {Post.objects.count()} posts in library."
            )
        )
