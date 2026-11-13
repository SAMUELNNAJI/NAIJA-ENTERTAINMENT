"""Views for The Nigerian Entrepreneur — one view per URL pattern."""
import re
import random
import logging
import secrets
import uuid
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.db.models import Count, Q, Sum
from django.http import Http404, HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from . import content
from .forms import CommentForm, SignupForm
from .models import Comment, EmailDelivery, NewsletterSubscriber, Post, PostDailyStat

logger = logging.getLogger(__name__)


def _resolve_href(href):
    """Resolve a content href ("#fragment", "/path/" or "url-name:arg")."""
    if href.startswith(("#", "/", "http:", "https:", "mailto:", "tel:")):
        return href
    name, _, arg = href.partition(":")
    return reverse(name, args=[arg]) if arg else reverse(name)


def _resolve_card(card):
    """Return a copy of *card* with its href resolved to a real URL."""
    card = dict(card)
    card["url"] = _resolve_href(card.pop("href"))
    return card


def _resolve_category(category):
    """Return a render-ready copy of a category page definition."""
    category = dict(category)
    category["hero_actions"] = [
        {**action, "url": _resolve_href(action["href"])}
        for action in category["hero_actions"]
    ]
    category["feature"] = _resolve_card(category["feature"])
    category["stack"] = [_resolve_card(card) for card in category["stack"]]
    category["more"] = [_resolve_card(card) for card in category["more"]]
    cta = dict(category["cta"])
    if not cta["form"]:
        cta["action"] = {**cta["action"], "url": _resolve_href(cta["action"]["href"])}
    category["cta"] = cta
    return category


def _post_cards(request, posts):
    """Shape DB posts like the static cards the templates already expect."""
    cards = []
    for post in posts:
        cards.append(
            {
                # Filter chips use category slugs. Keep editorial tags too so
                # a card can be found by either its category or a topic tag.
                "tags": f"{post.category} {post.tags}".strip(),
                "category": post.category,
                "url": post.get_absolute_url(),
                "image": post.image_url,
                "alt": post.image_alt or post.title,
                "tag": dict(Post.CATEGORY_CHOICES).get(post.category, post.category),
                "tag_class": "tag-blue",
                "title": post.title,
                "iso": post.published_at.strftime("%Y-%m-%d") if post.published_at else "",
                "date": post.published_at.strftime("%b %d, %Y") if post.published_at else "",
                "time": max(1, len(post.body.split()) // 200),
                "badge": "Featured" if post.is_featured else "Latest",
                "blurb": post.excerpt,
                "excerpt": post.excerpt,
                "is_external_image": post.is_external_image,
                "author": post.author_creator.name if post.author_creator else "Editorial",
            }
        )
    return cards


def home(request):
    ordered = Post.published().order_by("-published_at")

    # Each home filter is its own eleven-post database feed: a lead card plus
    # ten supporting cards. New published stories sort to the front.
    # Mix categories in a fresh order while always taking the newest item
    # available from each one first. This avoids an "All" feed dominated by
    # whichever category happened to receive the last batch of posts.
    category_order = [slug for slug, _label in Post.CATEGORY_CHOICES]
    random.shuffle(category_order)
    category_queues = {
        category: list(ordered.filter(category=category)) for category in category_order
    }
    all_posts = []
    while len(all_posts) < 11 and any(category_queues.values()):
        for category in category_order:
            if category_queues[category] and len(all_posts) < 11:
                all_posts.append(category_queues[category].pop(0))
    posts = _post_cards(request, all_posts)
    for card in posts:
        card["filter_tag"] = "all"

    filter_posts = []
    featured_posts = []
    for category, _label in Post.CATEGORY_CHOICES:
        category_cards = _post_cards(request, list(ordered.filter(category=category)[:11]))
        if not category_cards:
            continue
        for card in category_cards:
            card["filter_tag"] = category
        featured_posts.append(category_cards[0])
        filter_posts.extend(category_cards[1:])
    popular_posts = list(
        Post.published().order_by("-views", "-published_at")[:5]
    )
    return render(
        request,
        "pages/home.html",
        {
            "posts": posts,
            "filter_posts": filter_posts,
            "featured_posts": featured_posts,
            "popular_posts": popular_posts,
        },
    )


def category(request, slug):
    try:
        category_data = content.CATEGORIES[slug]
    except KeyError:
        raise Http404(f"Unknown category: {slug}")
    # Filter chips are real links (?filter=<chip>) and the server renders up
    # to fifteen matching articles, so every filter has a full page of cards
    # with its own featured spotlight — client-side filtering could only ever
    # see the first fifteen posts of the whole category.
    chip_values = [
        value for value, _ in category_data.get("chips", []) if value != "all"
    ]
    active_filter = (request.GET.get("filter") or "").strip().lower()
    chip_filtered = active_filter in chip_values
    if not chip_filtered:
        active_filter = "all"

    posts = Post.published().filter(category=slug).order_by("-published_at")
    if chip_filtered:
        matched = [
            post
            for post in posts
            if active_filter in set(re.split(r"[ ,]+", post.tags.lower()))
        ]
        # One spotlight + fourteen cards = fifteen articles per filter.
        db_posts = _post_cards(request, matched[:15])
    else:
        # Fifteen articles per category page: one spotlight, four beside it
        # and ten more behind the "Load more" button.
        db_posts = _post_cards(request, list(posts[:15]))

    category = _resolve_category(category_data)
    category["slug"] = slug
    ctx = {
        "category": category,
        "nav_active": category_data["nav_active"],
        "db_posts": db_posts,
        "active_filter": active_filter,
        "chip_filtered": chip_filtered,
    }
    return render(request, "pages/category.html", ctx)


def category_load_more(request, slug):
    """AJAX endpoint — returns the next batch of article cards as HTML fragments."""
    try:
        category_data = content.CATEGORIES[slug]
    except KeyError:
        return JsonResponse({"ok": False, "error": "Unknown category"}, status=404)

    PAGE_SIZE = 4
    try:
        page_num = max(1, int(request.GET.get("page", 1)))
    except (TypeError, ValueError):
        page_num = 1

    active_filter = (request.GET.get("filter") or "").strip().lower()
    chip_values = [v for v, _ in category_data.get("chips", []) if v != "all"]
    chip_filtered = active_filter in chip_values

    posts_qs = Post.published().filter(category=slug).order_by("-published_at")

    if chip_filtered:
        matched = [
            p for p in posts_qs
            if active_filter in set(re.split(r"[ ,]+", p.tags.lower()))
        ]
        all_cards = _post_cards(request, matched)
    else:
        all_cards = _post_cards(request, list(posts_qs))

    # The initial page already shows the first 15 (1 feature + 4 visible + 10 hidden).
    # Each subsequent AJAX call delivers PAGE_SIZE more, offset from position 15.
    INITIAL = 15
    start = INITIAL + (page_num - 1) * PAGE_SIZE
    batch = all_cards[start: start + PAGE_SIZE]
    has_more = len(all_cards) > start + PAGE_SIZE

    html_parts = []
    for article in batch:
        html_parts.append(
            render_to_string(
                "includes/mini_card.html",
                {"article": article, "hidden": False},
                request=request,
            )
        )

    return JsonResponse({
        "ok": True,
        "html": "".join(html_parts),
        "has_more": has_more,
        "next_page": page_num + 1,
    })


def page(request, slug):
    try:
        template = content.STATIC_PAGES[slug]
    except KeyError:
        raise Http404(f"Unknown page: {slug}")
    return render(request, template)


def article(request, slug):
    try:
        template = content.ARTICLES[slug]
    except KeyError:
        raise Http404(f"Unknown article: {slug}")
    return render(request, template)


def search(request):
    """Site-wide search across published posts (header panel + search page)."""
    q = (request.GET.get("q") or "").strip()
    results = Post.published().none()
    if q:
        results = Post.published().filter(
            Q(title__icontains=q)
            | Q(excerpt__icontains=q)
            | Q(tags__icontains=q)
            | Q(body__icontains=q)
        ).order_by("-published_at")
    return render(
        request,
        "pages/search.html",
        {
            "q": q,
            "results": _post_cards(request, results[:30]),
            "result_count": results.count(),
            "nav_active": "search",
        },
    )


def bad_request(request, exception=None):
    return render(request, "400.html", status=400)


def permission_denied(request, exception=None):
    return render(request, "403.html", status=403)


def page_not_found(request, exception=None):
    return render(request, "404.html", status=404)


def server_error(request):
    return render(request, "500.html", status=500)


# ---------------------------------------------------------------- blog ----

def blog_detail(request, slug):
    post = get_object_or_404(Post.published(), slug=slug)
    Post.objects.filter(pk=post.pk).update(views=post.views + 1)
    post.refresh_from_db()
    today = timezone.now().date()
    stat, created = PostDailyStat.objects.get_or_create(
        post=post, date=today, defaults={"views": 1}
    )
    if not created:
        PostDailyStat.objects.filter(pk=stat.pk).update(views=stat.views + 1)

    comments = (
        post.comments.filter(is_approved=True, parent=None).prefetch_related("replies")
    )
    for c in comments:
        _mark_edit_permission(c, request)
        for r in c.replies.all():
            _mark_edit_permission(r, request)
    for c in comments:
        _mark_edit_permission(c, request)
        for r in c.replies.all():
            _mark_edit_permission(r, request)
    return render(
        request,
        "pages/blog_detail.html",
        {
            "post": post,
            "comments": comments,
            "comment_count": post.comment_count,
            "comment_form": CommentForm(
                initial={"name": request.user.get_full_name() or request.user.username}
            )
            if request.user.is_authenticated
            else CommentForm(),
            "related": Post.published()
            .filter(category=post.category)
            .exclude(pk=post.pk)[:4],
        },
    )


def _can_manage_comment(request, comment) -> bool:
    """Authors, staff, and the originating guest browser may manage a comment."""
    user = request.user
    if user.is_authenticated and (comment.user == user or user.is_staff):
        return True
    return not comment.user_id and comment.pk in request.session.get("guest_comment_ids", [])


def _mark_edit_permission(comment, request) -> None:
    """Attach template-friendly permissions without exposing guest ownership."""
    comment.can_edit = _can_manage_comment(request, comment)


# ----------------------------------------------------- comments (AJAX) ----

def _comment_json(comment, request):
    return {
        "id": comment.pk,
        "name": comment.name,
        "initials": comment.initials,
        "body": comment.body,
        "created": comment.created_at.strftime("%b %d, %Y · %H:%M"),
        "parent": comment.parent_id,
        "can_edit": _can_manage_comment(request, comment),
        "can_delete": _can_manage_comment(request, comment),
    }


@require_POST
def comment_create(request, slug):
    post = get_object_or_404(Post.published(), slug=slug)
    form = CommentForm(request.POST)
    parent = None
    parent_id = request.POST.get("parent")
    if parent_id:
        parent = get_object_or_404(Comment, pk=parent_id, post=post)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.parent = parent
        if request.user.is_authenticated:
            comment.user = request.user
            comment.name = comment.name or request.user.username
        else:
            comment.name = comment.name or "Guest"
        comment.save()
        if not request.user.is_authenticated:
            guest_ids = request.session.get("guest_comment_ids", [])
            request.session["guest_comment_ids"] = list(dict.fromkeys([*guest_ids, comment.pk]))[-100:]
        _mark_edit_permission(comment, request)
        return JsonResponse(
            {
                "ok": True,
                "comment": _comment_json(comment, request),
                "comment_html": render_to_string(
                    "includes/comment_sticker.html",
                    {"comment": comment},
                    request=request,
                ),
            }
        )
    return JsonResponse({"ok": False, "errors": form.errors}, status=400)


@require_POST
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    allowed = _can_manage_comment(request, comment)
    if not allowed:
        return JsonResponse({"ok": False, "error": "Not allowed"}, status=403)
    form = CommentForm(
        {
            "name": comment.name,
            "email": comment.email,
            "body": request.POST.get("body", ""),
        },
        instance=comment,
    )
    if form.is_valid():
        comment = form.save()
        return JsonResponse(
            {"ok": True, "comment": _comment_json(comment, request)}
        )
    return JsonResponse({"ok": False, "errors": form.errors}, status=400)


@require_POST
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    allowed = _can_manage_comment(request, comment)
    if not allowed:
        return JsonResponse({"ok": False, "error": "Not allowed"}, status=403)
    comment.delete()
    return JsonResponse({"ok": True, "id": pk})



# ---------------------------------------------------------------- auth ----

def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    initial = {"join_as_creator": request.GET.get("as") == "creator"}
    form = SignupForm(request.POST or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        if form.cleaned_data.get("join_as_creator"):
            from .models import CreatorProfile

            CreatorProfile.objects.get_or_create(
                user=user, defaults={"display_name": user.first_name or user.username}
            )
        subscriber = None
        if form.cleaned_data.get("email_updates"):
            subscriber, created = NewsletterSubscriber.objects.get_or_create(
                email=user.email.lower(),
                defaults={"user": user, "is_active": False},
            )
            if not created and subscriber.user_id is None:
                subscriber.user = user
                subscriber.save(update_fields=["user"])
        from .email_service import (
            EmailDeliveryError,
            send_account_email,
            send_subscription_confirmation,
        )

        email_error = False
        for kind in ("welcome", "business_promo"):
            try:
                send_account_email(user, kind)
            except EmailDeliveryError:
                logger.exception("Signup %s email failed for user %s", kind, user.pk)
                email_error = True
        if subscriber and not subscriber.is_active:
            try:
                send_subscription_confirmation(subscriber)
            except EmailDeliveryError:
                logger.exception("Newsletter confirmation email failed for user %s", user.pk)
                email_error = True
        login(request, user)
        messages.success(request, "Welcome! Your account is ready.")
        if email_error:
            messages.warning(
                request,
                "Your account is ready, but some emails could not be sent. Please contact us if you need help.",
            )
        return redirect("dashboard")
    return render(
        request,
        "auth/signup.html",
        {"form": form, "nav_active": "signup"},
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("admin_panel" if request.user.is_staff else "dashboard")
    from .forms import LoginForm

    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        # Preserve an explicit destination (e.g. a protected page); otherwise
        # staff belong in the site-wide Admin Studio, not Creator Studio.
        return redirect(request.GET.get("next") or ("admin_panel" if user.is_staff else "dashboard"))
    return render(request, "auth/login.html", {"form": form, "nav_active": "login"})


def logout_view(request):
    from django.contrib.auth import logout

    logout(request)
    return redirect("home")


@require_POST
def subscribe(request):
    email = (request.POST.get("email") or "").strip()
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError

    try:
        validate_email(email)
    except ValidationError:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"ok": False, "error": "Enter a valid email address."}, status=400)
        messages.error(request, "Enter a valid email address.")
        return redirect(request.META.get("HTTP_REFERER", reverse("home")))
    subscriber, _created = NewsletterSubscriber.objects.get_or_create(
        email=email.lower(),
        defaults={
            "user": request.user if request.user.is_authenticated else None,
            "is_active": False,
        },
    )
    if not subscriber.is_active:
        from .email_service import EmailDeliveryError, send_subscription_confirmation

        if request.user.is_authenticated and subscriber.user_id is None:
            subscriber.user = request.user
            subscriber.save(update_fields=["user"])
        resend_after = timezone.now() - timedelta(minutes=10)
        if (
            subscriber.confirmation_sent_at is None
            or subscriber.confirmation_sent_at <= resend_after
        ):
            try:
                send_subscription_confirmation(subscriber)
            except EmailDeliveryError:
                logger.exception("Newsletter confirmation email failed for %s", subscriber.email)
                error = "We saved your request, but could not send the confirmation email. Please try again."
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return JsonResponse({"ok": False, "error": error}, status=503)
                messages.error(request, error)
                return redirect(request.META.get("HTTP_REFERER", reverse("home")))
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse(
            {
                "ok": True,
                "message": (
                    "You're subscribed to new story emails."
                    if subscriber.is_active
                    else "Check your inbox to confirm your story email subscription."
                ),
            }
        )
    messages.success(
        request,
        "You're subscribed to new story emails."
        if subscriber.is_active
        else "Check your inbox to confirm your story email subscription.",
    )
    return redirect(request.META.get("HTTP_REFERER", reverse("home")))


def confirm_subscription(request, token):
    subscriber = get_object_or_404(NewsletterSubscriber, unsubscribe_token=token)
    if not subscriber.is_active:
        subscriber.is_active = True
        subscriber.save(update_fields=["is_active"])
    return render(request, "emails/subscribed.html")


def unsubscribe(request, token):
    subscriber = get_object_or_404(NewsletterSubscriber, unsubscribe_token=token)
    if subscriber.is_active:
        subscriber.is_active = False
    subscriber.unsubscribe_token = uuid.uuid4()
    subscriber.confirmation_sent_at = None
    subscriber.save(update_fields=["is_active", "unsubscribe_token", "confirmation_sent_at"])
    EmailDelivery.objects.filter(
        unsubscribe_token=token,
        status="queued",
    ).delete()
    return render(request, "emails/unsubscribed.html")


@csrf_exempt
@require_POST
def run_post_email_automation(request):
    token = settings.EMAIL_AUTOMATION_TOKEN
    if not token:
        return HttpResponseNotFound()
    supplied_token = request.headers.get("Authorization", "")
    expected_token = f"Bearer {token}"
    if not secrets.compare_digest(supplied_token, expected_token):
        return JsonResponse({"ok": False, "error": "Not authorized."}, status=403)

    from .email_service import queue_post_engagement_emails

    sent, failed = queue_post_engagement_emails()
    return JsonResponse({"ok": True, "sent": sent, "failed_or_queued": failed})
