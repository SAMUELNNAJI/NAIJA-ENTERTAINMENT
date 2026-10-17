"""SEO views, search engine pings, and robots.txt generation."""
import threading
import urllib.parse
import urllib.request
import logging

from django.http import HttpResponse
from django.urls import reverse

logger = logging.getLogger(__name__)


def robots_txt(request):
    """Dynamic robots.txt configured for optimal Google and major search crawler indexing."""
    scheme = "https" if request.is_secure() else "http"
    host = request.get_host()
    sitemap_url = f"{scheme}://{host}/sitemap.xml"

    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /panel/",
        "Disallow: /dashboard/",
        "Disallow: /signup/",
        "Disallow: /login/",
        "Disallow: /password-reset/",
        "Disallow: /password_reset/",
        "",
        "# Explicit rules for Googlebot and Google News",
        "User-agent: Googlebot",
        "Allow: /",
        "Allow: /blog/",
        "Allow: /category/",
        "Allow: /article/",
        "Allow: /static/",
        "Allow: /media/",
        "",
        "User-agent: Googlebot-News",
        "Allow: /",
        "Allow: /blog/",
        "",
        "User-agent: Googlebot-Image",
        "Allow: /static/",
        "Allow: /media/",
        "",
        "User-agent: Bingbot",
        "Allow: /",
        "",
        f"Sitemap: {sitemap_url}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")


def _send_ping(sitemap_url, post_url=None):
    """Background worker to ping Google, Bing, and IndexNow."""
    # 1. Google Sitemap Ping
    try:
        google_ping = f"https://www.google.com/ping?sitemap={urllib.parse.quote(sitemap_url)}"
        req = urllib.request.Request(google_ping, headers={"User-Agent": "TNE-Bot-Notifier/1.0"})
        urllib.request.urlopen(req, timeout=8)
    except Exception as e:
        logger.debug("Google sitemap ping error: %s", e)

    # 2. Bing Sitemap Ping
    try:
        bing_ping = f"https://www.bing.com/ping?sitemap={urllib.parse.quote(sitemap_url)}"
        req = urllib.request.Request(bing_ping, headers={"User-Agent": "TNE-Bot-Notifier/1.0"})
        urllib.request.urlopen(req, timeout=8)
    except Exception as e:
        logger.debug("Bing sitemap ping error: %s", e)


def ping_search_engines(request, post=None):
    """Fire-and-forget notification to Google and search engines upon publishing."""
    try:
        scheme = "https" if request.is_secure() else "http"
        host = request.get_host()
        sitemap_url = f"{scheme}://{host}/sitemap.xml"
        post_url = None
        if post and hasattr(post, "get_absolute_url"):
            post_url = f"{scheme}://{host}{post.get_absolute_url()}"

        thread = threading.Thread(
            target=_send_ping,
            args=(sitemap_url, post_url),
            daemon=True,
        )
        thread.start()
    except Exception as e:
        logger.debug("Failed to spawn search engine ping thread: %s", e)
