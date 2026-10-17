"""RSS & Atom syndication feeds for real-time Google News and bot ingestion."""
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed
from django.urls import reverse

from .models import Post


class LatestPostsFeed(Feed):
    title = "The Nigerian Entrepreneur — Real Business Insights, Greater Opportunities"
    link = "/"
    description = (
        "Breaking Nigerian business news, funding announcements, startup journeys, "
        "personal finance guides, and technology analysis."
    )
    language = "en-ng"

    def items(self):
        return Post.objects.filter(status="published").select_related("author").order_by("-published_at")[:50]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.excerpt or (item.body[:300] + "...")

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.published_at or item.created_at

    def item_updateddate(self, item):
        return item.updated_at

    def item_author_name(self, item):
        if item.author:
            return item.author.get_full_name() or item.author.username
        return "TNE Editorial Team"

    def item_categories(self, item):
        cats = [item.get_category_display()]
        if item.tags:
            cats.extend([t.strip() for t in item.tags.split() if t.strip()])
        return cats


class LatestPostsAtomFeed(LatestPostsFeed):
    feed_type = Atom1Feed
    subtitle = LatestPostsFeed.description
