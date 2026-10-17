
"""Seed the site DB: users, creator profiles, blog posts, stats, comments.

Run once after migrating:

    python manage.py seed

Creates a staff superuser + one demo creator with published articles,
plus starter posts mapped from the old static cards.
"""
import random
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from core import content
from core.models import Comment, CreatorProfile, Post, PostDailyStat


AUTHOR = {
    "username": "ngozi",
    "password": "naija-creator-2025",
    "email": "ngozi@example.com",
    "display_name": "Ngozi Eze",
    "avatar_url": "",
}


class Command(BaseCommand):
    help = "Seed users, creator profile, blog posts, stats and comments."

    def handle(self, *args, **options):
        admin, _ = User.objects.get_or_create(
            username="admin", defaults={"email": "admin@example.com", "is_staff": True, "is_superuser": True}
        )
        admin.set_password("naija-admin-2025")
        admin.save()

        creator, created = User.objects.get_or_create(
            username=AUTHOR["username"], defaults={"email": AUTHOR["email"]}
        )
        if created:
            creator.set_password(AUTHOR["password"])
            creator.save()
        CreatorProfile.objects.get_or_create(
            user=creator,
            defaults={
                "display_name": AUTHOR["display_name"],
                "bio": "Finance writer covering savings, investing and business in Nigeria.",
            },
        )

        rng = random.Random(42)
        today = date.today()
        seeded = 0
        for slug, cat in content.CATEGORIES.items():
            feature = dict(cat["feature"])
            stack = [dict(a) for a in cat["stack"]]
            more = [dict(a) for a in cat["more"]]
            cards = [("feature", feature)] + [("card", a) for a in stack + more]
            for kind, card in cards:
                image = card.get("img", "").replace("assets/", "")
                title = card.get("title", "Untitled")
                if Post.objects.filter(title=title, category=slug).exists():
                    continue
                post = Post.objects.create(
                    author=creator,
                    title=title,
                    category=slug,
                    tags=card.get("tags", ""),
                    image_url=image or "img/photos/ideas.jpg",
                    image_alt=card.get("alt", title),
                    excerpt=card.get("blurb", ""),
                    body=self._body(card),
                    status="published",
                    is_featured=(kind == "feature"),
                    published_at=timezone.now() - timedelta(days=rng.randint(1, 40)),
                )
                for i in range(14):
                    PostDailyStat.objects.get_or_create(
                        post=post,
                        date=today - timedelta(days=i),
                        defaults={"views": rng.randint(5, 220)},
                    )
                seeded += 1

        first = Post.published().first()
        if first and not Comment.objects.filter(post=first).exists():
            Comment.objects.create(
                post=first, name="Adaeze Okafor", email="ada@example.com",
                body="This is exactly what I needed — the savings tips are gold. More on budgeting please!",
            )
            reply_to = Comment.objects.filter(post=first).first()
            Comment.objects.create(
                post=first, parent=reply_to, name="Ngozi Eze",
                email="ngozi@example.com",
                body="Thanks Adaeze! A deep-dive on budgeting templates is coming next week.",
            )
            Comment.objects.create(
                post=first, name="Tunde Bakare", email="tunde@example.com",
                body="Tried the 50/30/20 rule from this post and it actually works with my salary. Subscribed!",
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {seeded} posts. Login: admin / naija-admin-2025, "
                f"{AUTHOR['username']} / {AUTHOR['password']}"
            )
        )

    def _body(self, card):
        blurb = card.get("blurb", "")
        return (
            f"<p>{blurb}</p>"
            "<p>Starting a business in Nigeria takes more than capital — it takes clarity. "
            "This guide breaks the idea into steps you can act on this week: validate demand, "
            "price for profit, and build with the tools you already have.</p>"
            "<h2>Why this works in Nigeria</h2>"
            "<p>Local demand is strong, competition is uneven, and digital channels let a "
            "one-person team reach millions. Focus on a painful problem and charge fairly.</p>"
            "<h2>Next steps</h2>"
            "<ul><li>Talk to ten potential customers</li>"
            "<li>Launch the smallest paid version</li>"
            "<li>Reinvest the first profits into visibility</li></ul>"
        )