"""Top up the editorial library so every category has 15+ published posts.

The original library (replace_posts_with_editorial) seeded 42 articles.
This command adds the missing volume in the same voice and style, tags the
new pieces with real filter-chip values, and gives older articles at least
one chip tag so every category filter returns results.

Idempotent: existing titles are skipped, so it is safe to re-run.
"""
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import Post
from core.management.commands.replace_posts_with_editorial import IMAGES, article_body

# Chip values per category — mirrors the "chips" defined in core.content.
CHIPS = {
    "finance": ["investing", "personal", "savings", "banking", "tips"],
    "business": ["news", "strategy", "startups", "small", "tools"],
    "crypto": ["crypto", "web3", "blockchain", "defi", "nfts"],
    "entrepreneur": ["startups", "stories", "skills", "funding", "motivation"],
    "affiliates": ["marketing", "online", "programs", "guides"],
}

TARGET_PER_CATEGORY = 15

POSTS = [
    # ---- finance (+7) ----
    ("finance", "Dollar-Cost Averaging: A Calm Way to Invest Through Volatility", "investing tips", "Spreading investments across time takes the pressure off picking the perfect entry point — and keeps you invested."),
    ("finance", "Choosing a Nigerian Bank That Actually Fits Your Business", "banking small", "Compare charges, settlement speeds, transfer limits and support before you lock in a business account."),
    ("finance", "The 50/30/20 Budget, Adjusted for Naira Realities", "personal tips", "A simple allocation rule you can tune to current prices without abandoning your savings goals."),
    ("finance", "Where to Park Your Emergency Fund for Quick Access", "savings banking", "Balancing same-day access against returns so a real emergency never turns into debt."),
    ("finance", "How to Read a Mutual Fund Fact Sheet Before You Invest", "investing", "Fees, past returns, manager tenure and asset mix — the numbers that matter, on one page."),
    ("finance", "Seven Money Habits That Quietly Drain Your Account", "personal tips", "Small recurring charges and fuzzy spending rules add up. Here is how to spot and stop them."),
    ("finance", "Thrift Groups vs Digital Savings Apps: What Works Better?", "savings", "A candid comparison of discipline, risk and returns between esusu collectors and app-based savings."),
    # ---- business (+7) ----
    ("business", "Nigerian Businesses Are Embracing Automation — What It Means for Small Teams", "news tools", "From invoicing to inventory, affordable tools are changing how lean teams operate day to day."),
    ("business", "Bootstrapping vs Raising Funding: Choosing the Right Path for Your Stage", "startups strategy", "Control, speed and accountability — the trade-offs behind each growth financing route."),
    ("business", "How to Build a 90-Day Growth Strategy You Can Actually Track", "strategy", "Break the annual vision into a quarterly plan with one clear metric per goal."),
    ("business", "Inventory Mistakes That Quietly Kill Small Retail Businesses", "small", "Overstocking, blind spots and late reorders — and the simple checks that catch them early."),
    ("business", "The Small Business Owner's Guide to Social Media That Sells", "small tools", "Pick one channel, post with intent and turn attention into measurable conversations."),
    ("business", "Write a Standard Operating Procedure in One Afternoon", "tools strategy", "A lightweight template for documenting repeatable work so it survives your absence."),
    ("business", "Registering a Business in Nigeria: CAC Steps New Founders Should Know", "news startups", "Name reservation, registration types, taxes and the paperwork that keeps you compliant."),
    # ---- crypto (+6) ----
    ("crypto", "Stablecoins Are Becoming Africa's Rail for Cross-Border Payments", "crypto blockchain", "Why businesses are settling invoices in dollar-backed tokens — and what to watch before adopting them."),
    ("crypto", "How to Research a Web3 Project Before You Buy the Token", "web3 crypto", "Team, tokenomics, vesting, community and code — a pre-purchase checklist that filters hype."),
    ("crypto", "Understanding DeFi Yield: Where the Returns Actually Come From", "defi", "Lending spreads, fees and incentives explained — and why high APYs carry hidden risk."),
    ("crypto", "NFTs After the Hype: Real Utility in Ticketing and Membership", "nfts web3", "Beyond profile pictures: the use cases that survived the downturn and keep shipping."),
    ("crypto", "Self-Custody Basics: Keeping Your Crypto Keys Safe in Nigeria", "crypto", "Hardware wallets, seed-phrase hygiene and recovery drills that prevent permanent loss."),
    ("crypto", "What Blockchain Verification Really Means for Business Records", "blockchain", "Where distributed ledgers genuinely help with provenance, audits and trust between partners."),
    # ---- entrepreneur (+7) ----
    ("entrepreneur", "How a Lagos Baker Turned Weekend Orders into a National Brand", "stories motivation", "From kitchen-table cakes to a shipping-ready operation — the pivots that made it work."),
    ("entrepreneur", "From Campus Hustle to Full-Time Business: A Graduate's Story", "stories startups", "What changed when side income had to cover rent, salaries and taxes."),
    ("entrepreneur", "Public Speaking for Founders: Pitching Without the Panic", "skills", "Structure, rehearsal and breathing techniques that steady you before demo day."),
    ("entrepreneur", "Grant Funding vs Investor Funding: Which Fits Your Idea?", "funding", "Non-dilutive grants, angel cheques and accelerators compared on terms and expectations."),
    ("entrepreneur", "The Skill of Saying No: Protecting Your Time as a Founder", "motivation skills", "Every new opportunity feels urgent; focus is the discipline of choosing one."),
    ("entrepreneur", "Building a Team of One: Tools and Routines That Multiply You", "skills startups", "Automation, batching and checklists for founders doing five jobs at once."),
    ("entrepreneur", "Why Your First 100 Customers Matter More Than Your Business Plan", "startups motivation", "Early adopters teach you what no spreadsheet can — if you serve them deliberately."),
    # ---- affiliates (+6) ----
    ("affiliates", "How Affiliate Commissions Really Work: CPA, CPS and Recurring Models", "programs marketing", "The payment structures behind every offer, and how to match them to your content."),
    ("affiliates", "Turning TikTok Viewers into Affiliate Buyers Without Burning Trust", "marketing online", "Short-form funnels that sell honestly — disclosure, hooks and calls to action."),
    ("affiliates", "Email Lists for Affiliates: A Simple Funnel That Keeps Earning", "online guides", "Capture, nurture and convert — why owned audiences outlast social algorithms."),
    ("affiliates", "How to Pick Profitable Affiliate Programs in the Nigerian Market", "programs", "Commission depth, cookie windows, payout reliability and product fit."),
    ("affiliates", "SEO Basics for Affiliate Content That Ranks", "guides online", "Keyword intent, structure and internal links for articles that keep earning clicks."),
    ("affiliates", "Disclosure Done Right: Staying Trustworthy and Compliance-Ready", "guides marketing", "How to write honest disclosures that build authority instead of scaring readers."),
]


class Command(BaseCommand):
    help = "Add editorial posts so every category page has at least 15 published articles."

    def handle(self, *args, **options):
        now = timezone.now()
        created = 0
        for index, (category, title, tags, excerpt) in enumerate(POSTS):
            if Post.objects.filter(title=title).exists():
                continue
            Post.objects.create(
                title=title,
                category=category,
                tags=tags,
                image_url=IMAGES[category],
                image_alt=f"Illustration for {title}",
                excerpt=excerpt,
                body=article_body(title, category, excerpt),
                status="published",
                show_ads=True,
                published_at=now - timedelta(minutes=7 * (index + 1)),
            )
            created += 1
        self.stdout.write(self.style.SUCCESS(f"Created {created} new posts."))

        # Older library articles used free-form tags; make sure each one at
        # least matches one filter chip on its category page.
        tagged = 0
        for category, chips in CHIPS.items():
            chip_set = set(chips)
            for post in Post.published().filter(category=category):
                tokens = post.tags.lower().split()
                if chip_set.intersection(tokens):
                    continue
                chip = chips[tagged % len(chips)]
                post.tags = f"{post.tags} {chip}".strip()
                post.save(update_fields=["tags"])
                tagged += 1
        if tagged:
            self.stdout.write(
                self.style.SUCCESS(f"Added a filter-chip tag to {tagged} older posts.")
            )

        for category, label in Post.CATEGORY_CHOICES:
            count = Post.published().filter(category=category).count()
            line = f"{label} ({category}): {count} published"
            if count < TARGET_PER_CATEGORY:
                self.stderr.write(
                    self.style.WARNING(f"{line} — below target {TARGET_PER_CATEGORY}.")
                )
            else:
                self.stdout.write(f"{line}.")