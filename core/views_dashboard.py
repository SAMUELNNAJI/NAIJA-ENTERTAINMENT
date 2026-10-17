"""Dashboard views — creator studio and the admin control panel."""
import uuid
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from . import content
from .forms import PayoutAccountForm, PayoutRequestForm, PostForm, SponsorAdForm
from .models import Comment, CreatorProfile, PayoutRequest, Post, PostDailyStat, SponsorAd


def _creator_or_none(user):
    return getattr(user, "creator", None)


def _filter_tag_options():
    """Filter-chip values per category for the post form's tags section.

    Mirrors the chips each category page renders (core.content), minus the
    "all" pseudo-chip, so tags added here match the ?filter= values used by
    the site's chips.
    """
    options = []
    for slug, label in Post.CATEGORY_CHOICES:
        chips = [
            (value, text)
            for value, text in content.CATEGORIES.get(slug, {}).get("chips", [])
            if value != "all"
        ]
        if chips:
            options.append({"slug": slug, "label": label, "chips": chips})
    return options


def _apply_cover_upload(post, upload):
    """Persist an uploaded cover under MEDIA_ROOT and point the post at it."""
    if not upload:
        return
    ext = upload.name.rsplit(".", 1)[-1].lower()
    name = f"covers/{timezone.now():%Y%m%d}-{uuid.uuid4().hex[:8]}.{ext}"
    post.image_url = settings.MEDIA_URL + default_storage.save(name, upload)


# ------------------------------------------------------ creator studio ----

@login_required
def dashboard(request):
    if request.user.is_staff:
        return redirect("admin_panel")
    creator = _creator_or_none(request.user)
    if creator is None:
        # Every signed-in reader can publish immediately; do not strand them
        # on an activation-only page before they can reach their work.
        creator, _created = CreatorProfile.objects.get_or_create(
            user=request.user,
            defaults={"display_name": request.user.first_name or request.user.username},
        )

    posts = Post.objects.filter(author=request.user)
    published = posts.filter(status="published")

    # last-14-days views series for the chart
    today = timezone.now().date()
    days = [today - timedelta(days=i) for i in range(13, -1, -1)]
    stat_map = {
        s["date"]: s["views__sum"]
        for s in PostDailyStat.objects.filter(
            post__author=request.user, date__in=days
        )
        .values("date")
        .annotate(views__sum=Sum("views"))
    }
    views_series = [stat_map.get(d, 0) for d in days]

    category_rows = (
        published.values("category").annotate(n=Count("id")).order_by("-n")
    )

    ctx = {
        "nav_active": "dashboard",
        "creator": creator,
        "total_posts": posts.count(),
        "published_count": published.count(),
        "draft_count": posts.filter(status="draft").count(),
        "total_views": sum(p.views for p in posts),
        "ad_balance": creator.ad_balance,
        "estimated_total": sum(p.estimated_earnings for p in published),
        "comment_total": Comment.objects.filter(post__author=request.user).count(),
        "posts": posts[:10],
        "chart_labels": [d.strftime("%b %d") for d in days],
        "chart_views": views_series,
        "chart_categories": [
            dict(Post.CATEGORY_CHOICES).get(row["category"], row["category"])
            for row in category_rows
        ],
        "chart_category_counts": [row["n"] for row in category_rows],
    }
    return render(request, "dashboard/creator_studio/creator.html", ctx)


@login_required
def dashboard_post_new(request):
    if request.user.is_staff:
        return redirect("admin_panel_post_new")
    creator = _creator_or_none(request.user)
    if creator is None:
        creator = CreatorProfile.objects.create(
            user=request.user,
            display_name=request.user.first_name or request.user.username,
        )
    form = PostForm(request.POST or None, request.FILES or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        _apply_cover_upload(post, form.cleaned_data.get("cover_upload"))
        post.save()
        messages.success(request, f"“{post.title}” saved as {post.status}.")
        return redirect("dashboard")
    return render(
        request,
        "dashboard/creator_studio/post_form.html",
        {"form": form, "mode": "New post", "filter_options": _filter_tag_options()},
    )


@login_required
def dashboard_posts(request):
    """A full, dedicated list of the signed-in creator's stories."""
    if request.user.is_staff:
        return redirect("admin_panel_posts")
    creator, _created = CreatorProfile.objects.get_or_create(
        user=request.user,
        defaults={"display_name": request.user.first_name or request.user.username},
    )
    posts = Post.objects.filter(author=request.user).order_by("-updated_at")
    return render(
        request,
        "dashboard/creator_studio/posts.html",
        {"creator": creator, "posts": posts, "nav_active": "posts"},
    )


@login_required
def dashboard_post_edit(request, pk):
    if request.user.is_staff:
        return redirect("admin_panel_post_edit", pk=pk)
    post = get_object_or_404(Post, pk=pk)
    allowed = request.user.is_staff or post.author == request.user
    if not allowed:
        return redirect("dashboard")
    form = PostForm(
        request.POST or None,
        request.FILES or None,
        instance=post,
        user=request.user,
    )
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        _apply_cover_upload(post, form.cleaned_data.get("cover_upload"))
        post.save()
        messages.success(request, "Post updated.")
        return redirect("dashboard")
    return render(
        request,
        "dashboard/creator_studio/post_form.html",
        {
            "form": form,
            "mode": "Edit post",
            "post": post,
            "filter_options": _filter_tag_options(),
        },
    )


@login_required
def dashboard_post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    allowed = request.user.is_staff or post.author == request.user
    if allowed and request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted.")


@login_required
def payouts(request):
    if request.user.is_staff:
        return redirect("admin_panel_payouts")
    creator = _creator_or_none(request.user)
    if creator is None:
        return redirect("dashboard")
    account = getattr(creator, "payout_account", None)
    pending = sum(r.amount for r in creator.payout_requests.filter(status="pending"))
    available = max(creator.ad_balance - pending, 0)
    if request.method == "POST" and "save_account" in request.POST:
        account_form = PayoutAccountForm(request.POST, instance=account)
        if account_form.is_valid():
            item = account_form.save(commit=False); item.creator = creator; item.save(); messages.success(request, "Payout account saved."); return redirect("payouts")
    else: account_form = PayoutAccountForm(instance=account)
    if request.method == "POST" and "request_payout" in request.POST:
        request_form = PayoutRequestForm(request.POST)
        if not account: messages.error(request, "Add a payout account before requesting payment.")
        elif request_form.is_valid():
            payout = request_form.save(commit=False)
            if payout.amount <= 0 or payout.amount > available: request_form.add_error("amount", "Enter an amount within your available balance.")
            else: payout.creator=creator; payout.account=account; payout.save(); messages.success(request, "Payout request sent for review."); return redirect("payouts")
    else: request_form = PayoutRequestForm()
    return render(request, "dashboard/creator_studio/payouts.html", {"creator":creator,"account_form":account_form,"request_form":request_form,"available":available,"requests":creator.payout_requests.all()})


# ---------------------------------------------------------- admin panel ----

def _is_staff(user):
    return user.is_active and user.is_staff


@user_passes_test(_is_staff, login_url="login")
def admin_panel(request):
    posts = Post.objects.all()
    comments = Comment.objects.all()

    today = timezone.now().date()
    days = [today - timedelta(days=i) for i in range(13, -1, -1)]

    views_map = {
        s["date"]: s["views__sum"]
        for s in PostDailyStat.objects.filter(date__in=days)
        .values("date")
        .annotate(views__sum=Sum("views"))
    }
    comments_map = {
        s["created_at__date"]: s["n"]
        for s in comments.filter(created_at__date__in=days)
        .values("created_at__date")
        .annotate(n=Count("id"))
    }
    signups_map = {
        s["date_joined__date"]: s["n"]
        for s in User.objects.filter(date_joined__date__in=days)
        .values("date_joined__date")
        .annotate(n=Count("id"))
    }

    category_rows = (
        posts.filter(status="published")
        .values("category")
        .annotate(n=Count("id"))
        .order_by("-n")
    )
    top_posts = sorted(posts, key=lambda p: p.views, reverse=True)[:6]

    ctx = {
        "nav_active": "admin",
        "stats": {
            "users": User.objects.count(),
            "creators": CreatorProfile.objects.count(),
            "posts": posts.count(),
            "published": posts.filter(status="published").count(),
            "drafts": posts.filter(status="draft").count(),
            "comments": comments.count(),
            "pending_comments": comments.filter(is_approved=False).count(),
            "total_views": sum(p.views for p in posts),
        },
        "posts": posts[:15],
        "pending_comments": comments.filter(is_approved=False)[:10],
        "chart_labels": [d.strftime("%b %d") for d in days],
        "chart_views": [views_map.get(d, 0) for d in days],
        "chart_comments": [comments_map.get(d, 0) for d in days],
        "chart_signups": [signups_map.get(d, 0) for d in days],
        "chart_categories": [
            dict(Post.CATEGORY_CHOICES).get(row["category"], row["category"])
            for row in category_rows
        ],
        "chart_category_counts": [row["n"] for row in category_rows],
        "top_posts": top_posts,
    }
    return render(request, "dashboard/admin_studio/overview.html", ctx)


@user_passes_test(_is_staff, login_url="login")
def admin_panel_posts(request):
    posts = Post.objects.all()
    q = request.GET.get("q", "").strip()
    if q:
        posts = posts.filter(title__icontains=q)
    page_obj = Paginator(posts.select_related("author"), 20).get_page(request.GET.get("page"))
    return render(
        request,
        "dashboard/admin_studio/posts.html",
        {"posts": page_obj, "page_obj": page_obj, "q": q, "nav_active": "admin"},
    )


@user_passes_test(_is_staff, login_url="login")
def admin_panel_post_new(request):
    form = PostForm(request.POST or None, request.FILES or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        _apply_cover_upload(post, form.cleaned_data.get("cover_upload"))
        post.save()
        messages.success(request, f"“{post.title}” published to the site.")
        return redirect("admin_panel_posts")
    return render(
        request,
        "dashboard/admin_studio/post_form.html",
        {
            "form": form,
            "mode": "New blog post",
            "panel": "admin",
            "filter_options": _filter_tag_options(),
        },
    )


@user_passes_test(_is_staff, login_url="login")
def admin_panel_post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, request.FILES or None, instance=post, user=request.user)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        _apply_cover_upload(post, form.cleaned_data.get("cover_upload"))
        post.save()
        messages.success(request, "Post updated.")
        return redirect("admin_panel_posts")
    return render(request, "dashboard/admin_studio/post_form.html", {"form": form, "mode": "Edit blog post", "post": post, "panel": "admin", "filter_options": _filter_tag_options()})


@user_passes_test(_is_staff, login_url="login")
def admin_panel_toggle_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        if post.status == "published":
            post.status = "draft"
            post.published_at = None
        else:
            post.status = "published"
        post.save(update_fields=["status", "published_at"])
        messages.success(
            request,
            f"“{post.title}” is now {post.status} — it {'replaces' if post.status == 'published' else 'is hidden from'} the site's article cards.",
        )
    return redirect(request.META.get("HTTP_REFERER") or "admin_panel_posts")


@user_passes_test(_is_staff, login_url="login")
def admin_panel_toggle_featured(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.is_featured = not post.is_featured
        post.save(update_fields=["is_featured"])
        messages.success(request, f"Featured status updated for “{post.title}”.")
    return redirect(request.META.get("HTTP_REFERER") or "admin_panel_posts")


@user_passes_test(_is_staff, login_url="login")
def admin_panel_sponsors(request):
    form = SponsorAdForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Sponsor banner saved and is now available for rotation.")
        return redirect("admin_panel_sponsors")
    page_obj = Paginator(SponsorAd.objects.all(), 10).get_page(request.GET.get("page"))
    return render(request, "dashboard/admin_studio/sponsors.html", {"form": form, "ads": page_obj, "page_obj": page_obj, "nav_active": "admin"})


@user_passes_test(_is_staff, login_url="login")
def admin_panel_sponsor_toggle(request, pk):
    ad = get_object_or_404(SponsorAd, pk=pk)
    if request.method == "POST":
        ad.is_active = not ad.is_active
        ad.save(update_fields=["is_active"])
    return redirect("admin_panel_sponsors")


@user_passes_test(_is_staff, login_url="login")
def admin_panel_sponsor_edit(request, pk):
    ad = get_object_or_404(SponsorAd, pk=pk)
    form = SponsorAdForm(request.POST or None, instance=ad)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Sponsor banner updated.")
        return redirect("admin_panel_sponsors")
    return render(request, "dashboard/admin_studio/sponsor_edit.html", {"form": form, "ad": ad, "nav_active": "admin"})


@user_passes_test(_is_staff, login_url="login")
def admin_panel_post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted.")
    return redirect("admin_panel_posts")


@user_passes_test(_is_staff, login_url="login")
def admin_panel_comments(request):
    comments = Comment.objects.select_related("post", "user").order_by("-created_at")
    page_obj = Paginator(comments, 20).get_page(request.GET.get("page"))
    return render(
        request,
        "dashboard/admin_studio/comments.html",
        {"comments": page_obj, "page_obj": page_obj, "nav_active": "admin"},
    )


@user_passes_test(_is_staff, login_url="login")
def admin_panel_users(request):
    return render(request, "dashboard/admin_studio/users.html", {"users": User.objects.select_related("creator").order_by("-date_joined")})


@user_passes_test(_is_staff, login_url="login")
def admin_panel_payouts(request):
    return render(request, "dashboard/admin_studio/payouts.html", {"requests": PayoutRequest.objects.select_related("creator__user", "account")})


@user_passes_test(_is_staff, login_url="login")
def admin_panel_payout_action(request, pk, action):
    payout = get_object_or_404(PayoutRequest, pk=pk, status="pending")
    if request.method == "POST" and action in ("paid", "rejected"):
        if action == "paid":
            if payout.amount > payout.creator.ad_balance: messages.error(request, "Creator balance is too low."); return redirect("admin_panel_payouts")
            payout.creator.ad_balance -= payout.amount; payout.creator.save(update_fields=["ad_balance"])
        payout.status = action; payout.processed_at = timezone.now(); payout.save(update_fields=["status", "processed_at"]); messages.success(request, f"Payout marked {action}.")
    return redirect("admin_panel_payouts")


@user_passes_test(_is_staff, login_url="login")
def admin_panel_comment_toggle(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        comment.is_approved = not comment.is_approved
        comment.save(update_fields=["is_approved"])
    return redirect("admin_panel_comments")

    return redirect("dashboard")
