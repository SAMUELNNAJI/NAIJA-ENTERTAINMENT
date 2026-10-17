"""Assign a distinct topic-appropriate Unsplash cover image to every post."""
from django.core.management.base import BaseCommand
from core.models import Post


PHOTO_IDS = [
    "1554224155-8d04cb21cd6c", "1579621970563-ebec7560ff3e", "1556742049-0cfed4f6a45d", "1526304640581-d334cdbbf45e",
    "1563013544-824ae1b704d3", "1551836022-d5d88e9218df", "1554224154-26032ffc0d07", "1554224155-6726b3ff858f",
    "1454165804606-c3d57bc86b40", "1556761175-b413da4baf72", "1521737711867-e3b97375f902", "1497366811353-6870744d04b2",
    "1553877522-43269d4ea984", "1524758631624-e2822e304c36", "1552664730-d307ca884978", "1522071820081-009f0129c71c",
    "1639762681485-074b7f938ba0", "1642790106117-e829e14a795f", "1621761191319-c6fb62004040", "1622630998477-20aa696ecb05",
    "1621504450181-5d356f61d307", "1621416894569-0f39ed31d247", "1640340434855-6084b1f4901c", "1642790551116-18e150f248e5",
    "1516321318423-f06f85e504b3", "1498050108023-c5249f4df085", "1542744173-8e7e53415bb0", "1517048676732-d65bc937f952",
    "1519389950473-47ba0277781c", "1531497865144-0464ef8fb9a9", "1497215842964-222b430dc094", "1556761175-5973dc0f32e7",
    "1460925895917-afdab827c52f", "1551836022-4c4c79ecde51", "1499750310107-5fef28a66643", "1497366754035-f200968a6e72",
    "1551434678-e076c223a692", "1500530855697-b586d89ba3ee", "1533750349088-cd871a92f312", "1517245386807-bb43f82c33c4",
]


class Command(BaseCommand):
    help = "Give each existing post a distinct related cover image."

    def handle(self, *args, **options):
        posts = list(Post.objects.order_by("pk"))
        if len(posts) != len(PHOTO_IDS):
            self.stderr.write(self.style.ERROR(f"Expected {len(PHOTO_IDS)} posts, found {len(posts)}. No changes made."))
            return
        for post, photo_id in zip(posts, PHOTO_IDS):
            post.image_url = f"https://images.unsplash.com/photo-{photo_id}?auto=format&fit=crop&w=1400&q=80"
            post.image_alt = f"Cover image for {post.title}"
            post.save(update_fields=["image_url", "image_alt", "updated_at"])
        self.stdout.write(self.style.SUCCESS(f"Assigned {len(posts)} unique cover images."))
