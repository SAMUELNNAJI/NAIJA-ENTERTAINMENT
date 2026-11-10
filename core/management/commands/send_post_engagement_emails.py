from django.core.management.base import BaseCommand

from core.email_service import queue_post_engagement_emails


class Command(BaseCommand):
    help = (
        "Queue and send due low-view reminders, popular-post announcements, "
        "and retry queued post emails."
    )

    def handle(self, *args, **options):
        sent, failed = queue_post_engagement_emails()
        self.stdout.write(
            self.style.SUCCESS(
                f"Post email automation complete: {sent} sent, {failed} failed or still queued."
            )
        )
