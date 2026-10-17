"""Replace placeholder posts with a 40-piece original editorial library."""
from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import Post


IMAGES = {
    "finance": "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=1400&q=80",
    "business": "https://images.unsplash.com/photo-1556761175-b413da4baf72?auto=format&fit=crop&w=1400&q=80",
    "crypto": "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?auto=format&fit=crop&w=1400&q=80",
    "entrepreneur": "https://images.unsplash.com/photo-1521737711867-e3b97375f902?auto=format&fit=crop&w=1400&q=80",
    "affiliates": "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=1400&q=80",
}

POSTS = [
    ("finance", "How to Build a Personal Budget That Survives an Unpredictable Month", "budgeting savings cash-flow", "A flexible, zero-drama system for planning income, bills, savings and surprises."),
    ("finance", "Emergency Funds in Naira: Start Small, Protect Your Options", "emergency-fund savings naira", "Why a modest cash buffer can be more useful than a perfect investment plan."),
    ("finance", "Debt Without Panic: A Simple Plan for Paying What You Owe", "debt repayment personal-finance", "A clear way to list, prioritise and steadily reduce expensive debt."),
    ("finance", "Salary Day Systems: Give Every Naira a Job Before It Disappears", "salary budgeting money", "Turn payday into a repeatable routine instead of a month-long guessing game."),
    ("finance", "What to Check Before You Join a Savings or Investment Group", "investing due-diligence savings", "Questions to ask about custody, fees, risk and withdrawal rules before you contribute."),
    ("finance", "Side Income Is Not a Plan Until You Track the Numbers", "side-hustle income bookkeeping", "Separate revenue, costs and profit so a busy side project can become a real business."),
    ("finance", "A Beginner's Guide to Comparing Investment Risk", "investing risk returns", "How time horizon, liquidity and loss tolerance help you compare opportunities honestly."),
    ("finance", "The Monthly Money Review Every Entrepreneur Should Schedule", "cash-flow finance review", "A 30-minute monthly review to spot leaks, protect cash and make better decisions."),
    ("business", "The One-Page Business Plan That Helps You Start Before You Feel Ready", "business-plan startup strategy", "A focused planning page for your customer, offer, costs, channels and next experiment."),
    ("business", "Pricing a Service: Stop Guessing and Start Covering Your Costs", "pricing services profit", "Build a price around time, delivery costs, margin and the value your customer receives."),
    ("business", "How to Interview Customers Without Selling to Them", "customer-research validation", "Use open questions to learn what buyers actually struggle with before you build."),
    ("business", "Your First 10 Customers: A Better Goal Than Going Viral", "sales customers growth", "Small, direct outreach creates feedback and trust that broad attention cannot replace."),
    ("business", "A Practical Weekly Sales Pipeline for a Small Team", "sales pipeline operations", "A lightweight rhythm for leads, follow-ups, proposals and lessons from lost deals."),
    ("business", "When to Hire: Three Signs Your Business Needs Help", "hiring operations small-business", "Hire when recurring work has a clear process, not simply because the founder is exhausted."),
    ("business", "How to Write an Offer People Can Understand in Ten Seconds", "marketing offer copywriting", "Make the customer, outcome, proof and next step obvious on every sales page."),
    ("business", "Simple Bookkeeping Habits That Make Tax Time Less Stressful", "bookkeeping records tax", "Keep sales, expenses and evidence organised from day one with a weekly routine."),
    ("crypto", "Crypto Risk Management for Beginners: Rules Before Returns", "crypto risk investing", "A practical framework for position size, security and decisions you can live with."),
    ("crypto", "Before You Buy a Token, Read This Project Checklist", "crypto research tokens", "Look beyond hype: utility, supply, governance, liquidity and the team's public record."),
    ("crypto", "Wallet Security Basics: How to Reduce Avoidable Mistakes", "wallet security web3", "Protect recovery phrases, verify addresses and use deliberate transaction habits."),
    ("crypto", "Stablecoins Explained Without the Hype", "stablecoins crypto education", "What stablecoins aim to do, how they differ, and why issuer and reserve risk matter."),
    ("crypto", "Why 'Do Your Own Research' Needs a Process", "crypto research due-diligence", "A repeatable research log is more useful than social-media confidence."),
    ("crypto", "Web3 Careers: Skills You Can Build Before You Apply", "web3 careers skills", "Writing, design, community, analysis and development all have entry paths worth exploring."),
    ("crypto", "Avoiding Common Crypto Scams in Busy Markets", "crypto scams security", "Slow down around urgency, impersonation, guaranteed returns and unfamiliar links."),
    ("crypto", "How to Keep a Clean Record of Digital Asset Transactions", "crypto records taxes", "Transaction notes and exports make portfolio review and professional advice far easier."),
    ("entrepreneur", "From Skill to Service: Turning What You Know Into an Offer", "entrepreneurship services skills", "Package a useful skill around one problem, one customer and one clear outcome."),
    ("entrepreneur", "The Founder Habit That Makes Hard Weeks Easier", "founder habits productivity", "Create a weekly reset that turns scattered priorities into a short, realistic plan."),
    ("entrepreneur", "How to Test a Business Idea With a Small Pilot", "startup validation pilot", "Learn from a paid or tightly scoped test before investing in a full launch."),
    ("entrepreneur", "Building Confidence When You Are New to the Room", "confidence networking founders", "Preparation, curiosity and follow-through make networking more useful than performance."),
    ("entrepreneur", "A Better Way to Set Goals for a One-Person Business", "goals solopreneur strategy", "Use a few measurable operating goals instead of a long list of aspirations."),
    ("entrepreneur", "What Early-Stage Founders Should Put in Their First Pitch Deck", "pitch-deck startup funding", "Explain the problem, solution, customer, progress and use of funds with clarity."),
    ("entrepreneur", "Protecting Your Energy While Building Something New", "founder wellbeing productivity", "Simple boundaries and recovery habits can help you make better decisions over time."),
    ("entrepreneur", "How to Ask for Feedback That Makes Your Product Better", "feedback product customer", "Ask specific questions, listen without defending, then show people what changed."),
    ("affiliates", "Affiliate Marketing for Beginners: Start With Trust, Not Links", "affiliate marketing trust", "A durable affiliate strategy begins with useful recommendations for a defined audience."),
    ("affiliates", "How to Choose Affiliate Products You Can Recommend Honestly", "affiliate products audience", "Use products you understand, clear disclosures and a genuine customer fit."),
    ("affiliates", "Create Content That Helps Before It Asks for a Click", "affiliate content strategy", "Guides, comparisons and demonstrations earn attention more reliably than constant promotion."),
    ("affiliates", "Affiliate Disclosures: The Simple Practice That Builds Trust", "affiliate disclosure ethics", "Clear disclosure protects your audience and makes your recommendation more credible."),
    ("affiliates", "Measure Your Affiliate Content Without Chasing Vanity Metrics", "affiliate analytics conversions", "Track useful actions: qualified clicks, conversions, refund patterns and reader questions."),
    ("affiliates", "Email Lists for Affiliates: Build a Relationship You Own", "affiliate email marketing", "A welcome sequence and useful notes give you a direct channel beyond social algorithms."),
    ("affiliates", "How to Write a Helpful Product Comparison", "affiliate reviews content", "Compare the buyer, constraints, strengths and trade-offs—not just a feature list."),
    ("affiliates", "A 30-Day Content Plan for a New Affiliate Site", "affiliate content planning", "Publish a small, useful library around one problem before expanding your niche."),
]


def article_body(title, category, excerpt):
    category_note = {
        "finance": "Good financial decisions are usually less about finding a perfect answer and more about building a reliable routine.",
        "business": "The strongest small-business decisions come from direct customer evidence, not assumptions or noise.",
        "crypto": "Digital assets can be complex and volatile, so learning, security and position limits should come before confidence.",
        "entrepreneur": "Entrepreneurship rewards steady experiments: small actions, honest feedback and disciplined follow-through.",
        "affiliates": "Sustainable affiliate work is built on usefulness and disclosure; an audience can tell when a recommendation is earned.",
    }[category]
    return f"""<p>{excerpt}</p>
<h2>Start with the real problem</h2><p>{category_note} Before making a move, write down the outcome you want, the constraint you cannot ignore and the next action you can complete this week. That short list is more valuable than a complicated plan you will not revisit.</p>
<p>For <strong>{title.lower()}</strong>, begin by collecting a small amount of evidence. Review your current numbers, speak with the people affected and make the assumptions visible. A decision becomes easier to improve when you can explain why you made it.</p>
<h2>Use a simple operating system</h2><p>Choose one metric that reflects progress, one weekly habit that supports it and one checkpoint for reviewing what changed. Keep your records in a place you will actually use. Consistency makes patterns visible.</p>
<ul><li>Define the next useful outcome in plain language.</li><li>Set a limit for time, money or risk before you begin.</li><li>Review the result and adjust one thing at a time.</li></ul>
<h2>Make the next step small enough to finish</h2><p>You do not need to solve everything today. Pick a practical action, schedule it and learn from the result. Progress compounds when each small decision gives you better information for the next one.</p>
<blockquote>Clarity is not a feeling you wait for—it is a result you create by doing the next sensible thing.</blockquote>"""


class Command(BaseCommand):
    help = "Replace current posts with 40 original editorial articles and related cover images."

    def handle(self, *args, **options):
        posts = list(Post.objects.order_by("pk"))
        if len(posts) != len(POSTS):
            self.stderr.write(self.style.ERROR(f"Expected {len(POSTS)} posts, found {len(posts)}. No changes made."))
            return
        now = timezone.now()
        for index, (post, (category, title, tags, excerpt)) in enumerate(zip(posts, POSTS)):
            post.title = title
            post.slug = ""
            post.category = category
            post.tags = tags
            post.image_url = IMAGES[category]
            post.image_alt = f"Illustration for {title}"
            post.excerpt = excerpt
            post.body = article_body(title, category, excerpt)
            post.status = "published"
            post.is_featured = index < 5
            post.show_ads = True
            post.published_at = now
            post.save()
        self.stdout.write(self.style.SUCCESS(f"Replaced {len(posts)} posts with original editorial content."))
