import logging
import smtplib
from datetime import timedelta
from socket import timeout as SocketTimeout

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from django.utils import timezone

from .models import EmailDelivery, NewsletterSubscriber, Post

logger = logging.getLogger(__name__)


class EmailDeliveryError(Exception):
    """Raised when the configured email service cannot accept a message."""


def _send_template(subject, template, recipient, context):
    context = {"site_url": settings.PUBLIC_SITE_URL, **context}
    html = render_to_string(f"emails/{template}.html", context)
    text = "\n".join(
        line.strip()
        for line in strip_tags(html).splitlines()
        if line.strip()
    )
    message = EmailMultiAlternatives(
        subject=subject,
        body=text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient],
    )
    message.attach_alternative(html, "text/html")
    try:
        sent = message.send()
    except (smtplib.SMTPException, OSError, SocketTimeout) as exc:
        raise EmailDeliveryError(str(exc)) from exc
    if sent != 1:
        raise EmailDeliveryError("The email backend did not accept the message.")


def send_account_email(user, kind, amount=None):
    name = user.first_name or user.username
    templates = {
        "welcome": ("Welcome to The Nigerian Entrepreneur", "welcome"),
        "business_promo": ("Put your business in front of our audience", "business_promo"),
        "payout_requested": ("We received your payout request", "payout_requested"),
        "payout_paid": ("Your payout has been processed", "payout_paid"),
    }
    if kind not in templates:
        raise ValueError(f"Unknown account email kind: {kind}")
    subject, template = templates[kind]
    _send_template(
        subject,
        template,
        user.email,
        {"name": name, "user": user, "amount": amount},
    )


def send_subscription_confirmation(subscriber):
    confirm_url = (
        f"{settings.PUBLIC_SITE_URL}"
        f"{reverse('confirm_subscription', args=[subscriber.unsubscribe_token])}"
    )
    _send_template(
        "Confirm your TNE story emails",
        "subscription_confirmation",
        subscriber.email,
        {"confirm_url": confirm_url},
    )
    subscriber.confirmation_sent_at = timezone.now()
    subscriber.save(update_fields=["confirmation_sent_at"])


def send_admin_payout_email(payout, recipients):
    failed_recipients = []
    for recipient in recipients:
        try:
            _send_template(
                f"Payout request received — {payout.creator.name}",
                "payout_admin",
                recipient,
                {"payout": payout, "creator": payout.creator, "account": payout.account},
            )
        except EmailDeliveryError:
            logger.exception(
                "Admin payout notification failed for request %s to %s.",
                payout.pk,
                recipient,
            )
            failed_recipients.append(recipient)
    if failed_recipients:
        raise EmailDeliveryError(
            f"Could not notify {len(failed_recipients)} admin payout inbox(es)."
        )


def queue_post_email(post, kind, subscribers=None):
    if kind == "low_views":
        if post.author_id and post.author.email:
            EmailDelivery.objects.get_or_create(
                post=post,
                kind=kind,
                recipient_email=post.author.email,
            )
        return

    if kind not in ("new_post", "high_performance"):
        raise ValueError(f"Unknown post email kind: {kind}")
    subscribers = subscribers or NewsletterSubscriber.objects.filter(is_active=True)
    for subscriber in subscribers.iterator():
        if not subscriber.email:
            continue
        EmailDelivery.objects.get_or_create(
            post=post,
            kind=kind,
            recipient_email=subscriber.email,
            defaults={"unsubscribe_token": subscriber.unsubscribe_token},
        )


def dispatch_pending_email_deliveries(limit=500):
    sent_count = 0
    failed_count = 0
    for delivery in EmailDelivery.objects.filter(status="queued").select_related(
        "post", "post__author"
    ).order_by("created_at")[:limit]:
        post = delivery.post
        unsubscribe_url = ""
        if delivery.unsubscribe_token:
            unsubscribe_url = (
                f"{settings.PUBLIC_SITE_URL}"
                f"{reverse('unsubscribe', args=[delivery.unsubscribe_token])}"
            )
        context = {
            "post": post,
            "author_name": (
                post.author.first_name or post.author.username
                if post.author_id
                else "The Editorial Team"
            ),
            "post_url": f"{settings.PUBLIC_SITE_URL}{post.get_absolute_url()}",
            "unsubscribe_url": unsubscribe_url,
            "views": post.views,
        }
        email_details = {
            "new_post": (f"New story: {post.title}", "new_post"),
            "low_views": ("A few ideas to help your story reach more readers", "low_views"),
            "high_performance": (f"Trending now: {post.title}", "high_performance"),
        }
        subject, template = email_details[delivery.kind]
        try:
            _send_template(subject, template, delivery.recipient_email, context)
        except EmailDeliveryError as exc:
            delivery.attempts += 1
            delivery.last_error = str(exc)[:500]
            delivery.save(update_fields=["attempts", "last_error"])
            logger.error(
                "Email delivery %s failed for %s: %s",
                delivery.pk,
                delivery.recipient_email,
                exc,
            )
            failed_count += 1
        else:
            delivery.status = "sent"
            delivery.sent_at = timezone.now()
            delivery.last_error = ""
            delivery.save(update_fields=["status", "sent_at", "last_error"])
            sent_count += 1
    return sent_count, failed_count


def queue_post_engagement_emails():
    now = timezone.now()
    low_age = timedelta(days=settings.LOW_POST_MIN_AGE_DAYS)
    low_posts = Post.published().filter(
        published_at__lte=now - low_age,
        views__lt=settings.LOW_POST_VIEW_THRESHOLD,
    ).exclude(email_deliveries__kind="low_views")
    for post in low_posts.select_related("author").iterator():
        queue_post_email(post, "low_views")

    high_posts = Post.published().filter(
        views__gte=settings.HIGH_PERFORMANCE_VIEW_THRESHOLD,
    ).exclude(email_deliveries__kind="high_performance")
    for post in high_posts.iterator():
        queue_post_email(post, "high_performance")

    return dispatch_pending_email_deliveries()


def notify_new_post(post):
    queue_post_email(post, "new_post")
    return dispatch_pending_email_deliveries()
