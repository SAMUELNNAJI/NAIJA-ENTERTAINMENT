"""Sitemaps for search engines (Googlebot, Bingbot)."""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from . import content
from .models import Post


class PostSitemap(Sitemap):
    """Dynamic sitemap for all published editorial and creator posts."""
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return Post.objects.filter(status="published").order_by("-published_at")

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class CategorySitemap(Sitemap):
    """Sitemap for all top-level category verticals."""
    changefreq = "daily"
    priority = 0.85

    def items(self):
        return [slug for slug, _ in Post.CATEGORY_CHOICES]

    def location(self, item):
        return reverse("category", args=[item])


class StaticArticleSitemap(Sitemap):
    """Sitemap for deep long-form cornerstone guides and pillar content."""
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return list(content.ARTICLES.keys())

    def location(self, item):
        return reverse("article", args=[item])


class StaticViewSitemap(Sitemap):
    """Sitemap for key platform views and utility tools."""
    priority = 0.75
    changefreq = "weekly"

    def items(self):
        return [
            "home",
            "search",
            "currency_converter",
            "markets",
            "signup",
            "login",
        ]

    def location(self, item):
        return reverse(item)


class StaticPageSitemap(Sitemap):
    """Sitemap for institutional pages."""
    priority = 0.6
    changefreq = "monthly"

    def items(self):
        return list(content.STATIC_PAGES.keys())

    def location(self, item):
        return reverse("page", args=[item])


sitemaps = {
    "posts": PostSitemap,
    "categories": CategorySitemap,
    "articles": StaticArticleSitemap,
    "static": StaticViewSitemap,
    "pages": StaticPageSitemap,
}
