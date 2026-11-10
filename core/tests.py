from decimal import Decimal
from datetime import timedelta

from django.core import mail
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .email_service import notify_new_post, queue_post_engagement_emails
from .models import (
    CreatorProfile,
    EmailDelivery,
    NewsletterSubscriber,
    PayoutAccount,
    PayoutRequest,
    Post,
    estimate_view_earnings,
)


class ViewEarningsTests(SimpleTestCase):
    def test_one_hundred_views_earn_fifty_naira(self):
        self.assertEqual(estimate_view_earnings(100), Decimal("50.00"))
        self.assertEqual(Post(views=100).estimated_earnings, Decimal("50.00"))

    def test_partial_and_thousand_view_earnings(self):
        self.assertEqual(estimate_view_earnings(1), Decimal("0.50"))
        self.assertEqual(estimate_view_earnings(1000), Decimal("500.00"))


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    PUBLIC_SITE_URL="https://thenigerianentrepreneur.com",
    ADMIN_NOTIFICATION_EMAILS=["finance@example.com"],
)
class EmailWorkflowTests(TestCase):
    def setUp(self):
        mail.outbox = []

    def make_user(self, username, email, **kwargs):
        from django.contrib.auth.models import User

        return User.objects.create_user(
            username=username,
            email=email,
            password="test-password-123",
            **kwargs,
        )

    def make_post(self, author, title, views, published_at=None):
        return Post.objects.create(
            author=author,
            title=title,
            category="business",
            body="<p>Useful business advice.</p>",
            excerpt="A practical story.",
            status="published",
            views=views,
            published_at=published_at or timezone.now(),
        )

    def test_signup_sends_welcome_and_business_promotion(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "new-creator",
                "first_name": "Ada",
                "email": "ada@example.com",
                "password1": "Strong-test-password-2026",
                "password2": "Strong-test-password-2026",
                "email_updates": "on",
            },
        )

        self.assertRedirects(response, reverse("dashboard"))
        self.assertEqual(len(mail.outbox), 3)
        self.assertIn("Welcome", mail.outbox[0].subject)
        self.assertIn("business", mail.outbox[1].subject.lower())
        self.assertTrue(mail.outbox[0].alternatives)
        subscriber = NewsletterSubscriber.objects.get(email="ada@example.com")
        self.assertFalse(subscriber.is_active)
        self.assertIn("Confirm", mail.outbox[2].subject)
        self.client.get(
            reverse("confirm_subscription", args=[subscriber.unsubscribe_token])
        )
        subscriber.refresh_from_db()
        self.assertTrue(subscriber.is_active)

    def test_signup_does_not_subscribe_without_opt_in(self):
        self.client.post(
            reverse("signup"),
            {
                "username": "reader-no-mail",
                "email": "reader-no-mail@example.com",
                "password1": "Strong-test-password-2026",
                "password2": "Strong-test-password-2026",
            },
        )
        self.assertFalse(
            NewsletterSubscriber.objects.filter(
                email="reader-no-mail@example.com"
            ).exists()
        )

    def test_newsletter_subscribe_endpoint_validates_and_saves(self):
        invalid = self.client.post(
            reverse("subscribe"),
            {"email": "not-an-email"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(invalid.status_code, 400)
        self.assertFalse(NewsletterSubscriber.objects.exists())

        valid = self.client.post(
            reverse("subscribe"),
            {"email": "reader@example.com"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(valid.status_code, 200)
        self.assertEqual(valid.json()["ok"], True)
        subscriber = NewsletterSubscriber.objects.get(email="reader@example.com")
        self.assertFalse(subscriber.is_active)
        self.assertIn("confirm", valid.json()["message"].lower())
        self.assertEqual(len(mail.outbox), 1)
        self.client.post(
            reverse("subscribe"),
            {"email": "reader@example.com"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(len(mail.outbox), 1)
        self.client.get(
            reverse("confirm_subscription", args=[subscriber.unsubscribe_token])
        )
        subscriber.refresh_from_db()
        self.assertTrue(subscriber.is_active)

    def test_password_reset_sends_branded_html_email(self):
        self.make_user("reset-user", "reset@example.com")

        response = self.client.post(
            reverse("password_reset"), {"email": "reset@example.com"}
        )

        self.assertRedirects(response, reverse("password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Reset your password", mail.outbox[0].subject)
        self.assertTrue(mail.outbox[0].alternatives)
        self.assertIn("password-reset-confirm", mail.outbox[0].alternatives[0][0])

    @override_settings(EMAIL_AUTOMATION_TOKEN="long-test-automation-token")
    def test_email_automation_endpoint_requires_bearer_token(self):
        response = self.client.post(reverse("run_post_email_automation"))
        self.assertEqual(response.status_code, 403)

        response = self.client.post(
            reverse("run_post_email_automation"),
            HTTP_AUTHORIZATION="Bearer long-test-automation-token",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"ok": True, "sent": 0, "failed_or_queued": 0})

    def test_newsletter_signup_delivers_post_and_unsubscribe_works(self):
        subscriber = NewsletterSubscriber.objects.create(
            email="reader@example.com", is_active=True
        )
        author = self.make_user("writer", "writer@example.com")
        post = self.make_post(author, "A new business idea", 5)

        sent, failed = notify_new_post(post)

        self.assertEqual((sent, failed), (1, 0))
        delivery = EmailDelivery.objects.get(post=post, kind="new_post")
        self.assertEqual(delivery.status, "sent")
        self.assertIn(post.title, mail.outbox[0].subject)

        response = self.client.get(
            reverse("unsubscribe", args=[subscriber.unsubscribe_token])
        )

        self.assertEqual(response.status_code, 200)
        subscriber.refresh_from_db()
        self.assertFalse(subscriber.is_active)
        self.assertNotEqual(
            subscriber.unsubscribe_token,
            delivery.unsubscribe_token,
        )

    @override_settings(
        LOW_POST_MIN_AGE_DAYS=7,
        LOW_POST_VIEW_THRESHOLD=100,
        HIGH_PERFORMANCE_VIEW_THRESHOLD=1000,
    )
    def test_daily_job_sends_one_low_view_and_one_popular_post_email(self):
        author = self.make_user("low-author", "author@example.com")
        subscriber = NewsletterSubscriber.objects.create(
            email="fan@example.com", is_active=True
        )
        old_post = self.make_post(
            author,
            "Share this story",
            20,
            published_at=timezone.now() - timedelta(days=8),
        )
        popular_post = self.make_post(
            author,
            "A popular story",
            1000,
            published_at=timezone.now() - timedelta(days=2),
        )

        sent, failed = queue_post_engagement_emails()

        self.assertEqual((sent, failed), (2, 0))
        self.assertEqual(EmailDelivery.objects.filter(status="sent").count(), 2)
        self.assertEqual(len(mail.outbox), 2)
        self.assertTrue(
            EmailDelivery.objects.filter(post=old_post, kind="low_views").exists()
        )
        self.assertTrue(
            EmailDelivery.objects.filter(
                post=popular_post,
                kind="high_performance",
                recipient_email=subscriber.email,
            ).exists()
        )

        queue_post_engagement_emails()
        self.assertEqual(len(mail.outbox), 2)

    def test_payout_emails_user_admin_and_paid_confirmation(self):
        user = self.make_user("paid-creator", "creator@example.com")
        creator = CreatorProfile.objects.create(user=user, ad_balance=Decimal("300.00"))
        account = PayoutAccount.objects.create(
            creator=creator,
            bank_name="Example Bank",
            account_name="Creator Name",
            account_number="1234567890",
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse("payouts"), {"request_payout": "", "amount": "125.00"}
        )

        self.assertRedirects(response, reverse("payouts"))
        payout = PayoutRequest.objects.get(creator=creator)
        self.assertEqual(len(mail.outbox), 2)
        self.assertIn("payout request", mail.outbox[0].subject.lower())
        self.assertIn("Payout request received", mail.outbox[1].subject)

        admin = self.make_user("site-admin", "admin@example.com", is_staff=True)
        self.client.force_login(admin)
        response = self.client.post(
            reverse("admin_panel_payout_action", args=[payout.pk, "paid"])
        )

        self.assertRedirects(response, reverse("admin_panel_payouts"))
        self.assertEqual(len(mail.outbox), 3)
        self.assertIn("processed", mail.outbox[2].subject.lower())
        self.assertIn("125.00", mail.outbox[2].alternatives[0][0])

    def test_over_balance_payout_does_not_send_confirmation_or_create_request(self):
        user = self.make_user("low-balance", "low-balance@example.com")
        creator = CreatorProfile.objects.create(user=user, ad_balance=Decimal("50.00"))
        PayoutAccount.objects.create(
            creator=creator,
            bank_name="Example Bank",
            account_name="Creator Name",
            account_number="1234567890",
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse("payouts"), {"request_payout": "", "amount": "125.00"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(PayoutRequest.objects.filter(creator=creator).exists())
        self.assertEqual(len(mail.outbox), 0)
