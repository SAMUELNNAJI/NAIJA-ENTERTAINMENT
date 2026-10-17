"""Models for The Nigerian Entrepreneur.

These models power the blog (posts replace the old static article cards),
comments, creators and the dashboards. Content-driven archive pages still
live in core/content.py.
"""
from __future__ import annotations

import re

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


def _slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug or "post"


class CreatorProfile(models.Model):
    """A user who signed up to publish blogs and earn ad revenue."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="creator")
    display_name = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)
    avatar_url = models.URLField(blank=True)
    # Ad revenue share accrues here (NGN); admin can adjust manually.
    ad_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    rpm = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=950,
        help_text="Estimated NGN revenue per 1,000 post views.",
    )
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.display_name or self.user.get_username()

    @property
    def name(self) -> str:
        return self.display_name or self.user.get_full_name() or self.user.username


class Post(models.Model):
    """A blog post — written by a creator or the site (staff) account."""

    CATEGORY_CHOICES = [
        ("finance", "Finance"),
        ("business", "Business"),
        ("crypto", "Crypto / Web 3.0"),
        ("entrepreneur", "Entrepreneur Corner"),
        ("affiliates", "Affiliates"),
    ]
    STATUS_CHOICES = [("draft", "Draft"), ("published", "Published")]

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts", null=True, blank=True
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    tags = models.CharField(
        max_length=120,
        blank=True,
        help_text="Space-separated filter tags, e.g. 'investing personal'.",
    )
    image_url = models.CharField(
        max_length=200,
        default="img/photos/ideas.jpg",
        help_text="Static path under assets/ or a full https:// URL.",
    )
    image_alt = models.CharField(max_length=200, blank=True)
    excerpt = models.TextField(blank=True)
    body = models.TextField(help_text="Article HTML paragraphs.")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    is_featured = models.BooleanField(default=False)
    show_ads = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = _slugify(self.title)
            slug, n = base, 2
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        if self.status == "published" and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("blog_detail", args=[self.slug])

    @property
    def reading_time(self) -> int:
        """Estimated reading time in minutes for compact article listings."""
        return max(1, len(self.body.split()) // 200)

    @property
    def url(self) -> str:
        return self.get_absolute_url()

    @property
    def is_external_image(self) -> bool:
        # Anything but a static-relative path is rendered as-is: full URLs,
        # protocol-relative URLs and root-relative uploads (/media/covers/…).
        return self.image_url.startswith(("http://", "https://", "//", "/"))

    @property
    def author_creator(self):
        return getattr(self.author, "creator", None)

    @property
    def estimated_earnings(self):
        """100 views/impression is 10 Naira (0.10 NGN per view/impression)."""
        return (self.views / 100.0) * 10.0


    @property
    def comment_count(self) -> int:
        return Comment.objects.filter(post=self, is_approved=True).count()

    @classmethod
    def published(cls):
        return cls.objects.filter(status="published")


class PostDailyStat(models.Model):
    """Per-day view counts — powers the dashboard charts."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="daily_stats")
    date = models.DateField()
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-date"]
        unique_together = [("post", "date")]

    def __str__(self) -> str:
        return f"{self.post.slug} {self.date}: {self.views}"


class Comment(models.Model):
    """Threaded comments (one reply level) — managed over AJAX."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="comments"
    )
    name = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    body = models.TextField(max_length=4000)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"{self.name} on {self.post.slug}"

    @property
    def initials(self) -> str:
        parts = [p for p in self.name.split() if p][:2]
        return "".join(p[0].upper() for p in parts) or "?"

    @property
    def is_parent(self) -> bool:
        return self.parent_id is None

    def editable_by(self, user) -> bool:
        if not user or not user.is_authenticated:
            return False
        return (self.user and self.user == user) or user.is_staff

    @property
    def is_parent(self) -> bool:
        """True when this is a top-level comment (not a reply)."""
        return self.parent_id is None

    def editable_by(self, user) -> bool:
        if not user or not user.is_authenticated:
            return False
        return (self.user and self.user == user) or user.is_staff


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.email


class SponsorAd(models.Model):
    """A site-wide sponsor campaign managed from the admin panel."""
    title = models.CharField(max_length=140)
    image_url = models.CharField(max_length=500, help_text="Image URL or path under assets/.")
    redirect_url = models.URLField(help_text="Where the banner opens when clicked.")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def is_external_image(self):
        return self.image_url.startswith(("http://", "https://", "//", "/"))


class PayoutAccount(models.Model):
    creator = models.OneToOneField(CreatorProfile, on_delete=models.CASCADE, related_name="payout_account")
    bank_name = models.CharField(max_length=120)
    account_name = models.CharField(max_length=120)
    account_number = models.CharField(max_length=20)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.creator} — {self.bank_name}"


class PayoutRequest(models.Model):
    STATUS_CHOICES = [("pending", "Pending"), ("paid", "Paid"), ("rejected", "Rejected")]
    creator = models.ForeignKey(CreatorProfile, on_delete=models.CASCADE, related_name="payout_requests")
    account = models.ForeignKey(PayoutAccount, on_delete=models.PROTECT, related_name="requests")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    note = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]


class Notification(models.Model):
    """User notifications (e.g. editorial actions, post removal, payout alerts)."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=200, default="Important Notice")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} — {self.title}"
