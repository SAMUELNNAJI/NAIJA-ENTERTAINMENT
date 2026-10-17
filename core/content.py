"""
Site content for The Nigerian Entrepreneur.

Ported from the legacy Node generator (tools/content-categories.mjs) so the
category archive pages can be driven by one shared Django template
(templates/pages/category.html) instead of five generated copies.

Link conventions
----------------
Card/action hrefs are stored as either:

  - a literal fragment or absolute URL ("#latest", "https://…"), or
  - "url-name:arg" (e.g. "category:finance"), which core.views resolves with
    django.urls.reverse() at render time.

Image paths are relative to assets/ (the STATICFILES_DIRS entry), so they are
rendered with {% static 'img/photos/…' %}.
"""


def feature(tags, image, alt, title, blurb, author, iso, date, minutes):
    """Spotlight card at the top of a category page."""
    return {
        "tags": tags,
        "href": "article:10-profitable-business-ideas",
        "image": image,
        "alt": alt,
        "badge": "Featured",
        "title": title,
        "blurb": blurb,
        "author": author,
        "iso": iso,
        "date": date,
        "time": minutes,
    }


def card(tags, image, alt, tag_class, tag, title, iso, date, minutes, href):
    """Small article card used in the category stacks."""
    return {
        "tags": tags,
        "href": href,
        "image": image,
        "alt": alt,
        "tag_class": tag_class,
        "tag": tag,
        "title": title,
        "iso": iso,
        "date": date,
        "time": minutes,
    }


def link_cta(label, href, css="btn btn--light"):
    """Hero action rendered as a plain button link."""
    return {"label": label, "href": href, "class": css}

# SVG icons for the category CTA bands (kept inline, as in the original).
_ICON_CHART = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 17l5-6 4 4 5-8 4 5"/><path d="M3 21h18"/></svg>'
_ICON_BARS = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 20h18M7 20V10M12 20V4M17 20v-7"/></svg>'
_ICON_CLOCK = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>'
_ICON_BOLT = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M13 2 4 14h6l-1 8 9-12h-6z"/></svg>'
_ICON_SHARE = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M17 3h4v4"/><path d="M21 3 11 13"/><path d="M8 21H5a2 2 0 0 1-2-2v-3M15 21h4a2 2 0 0 0 2-2v-3"/></svg>'


def _subscribe_cta(modifier, icon, title, text):
    """CTA band with the inline newsletter form."""
    return {
        "modifier": modifier,
        "icon": icon,
        "title": title,
        "text": text,
        "form": True,
    }


def _link_band(modifier, icon, title, text, label, href):
    """CTA band with a single call-to-action button."""
    return {
        "modifier": modifier,
        "icon": icon,
        "title": title,
        "text": text,
        "form": False,
        "action": {"label": label, "href": href},
    }


CATEGORIES: dict = {}


CATEGORIES["finance"] = {
    "nav_active": "finance",
    "page_id": "finance",
    "meta_title": "Finance — Practical financial tips, tools and resources",
    "meta_description": (
        "Learn how to budget, save, invest and grow your money in Nigeria with "
        "practical guides on personal finance, savings, banking and wealth building."
    ),
    "theme": "t-finance",
    "image": "img/photos/coins.jpg",
    "image_alt": "Coin stacks with a growing plant",
    "crumb": "Finance",
    "heading": "Finance",
    "blurb": (
        "Practical financial tips, investment strategies, and tools to help you "
        "manage, grow and protect your money. Learn how to build wealth and "
        "financial freedom as a Nigerian entrepreneur."
    ),
    "hero_actions": [
        link_cta("Browse Articles", "#latest"),
        link_cta("Crypto &amp; Web3", "category:crypto", "btn btn--outline-light"),
    ],
    "chips": [
        ("all", "All"),
        ("investing", "Investing"),
        ("personal", "Personal Finance"),
        ("savings", "Savings"),
        ("banking", "Banking"),
        ("tips", "Financial Tips"),
    ],
    "feature": feature(
        "investing personal",
        "img/photos/desk.jpg",
        "Notebook, pen and savings jar on a study desk",
        "How to Build a Solid Investment Portfolio in Nigeria",
        (
            "Learn the investment options available to you, asset management tips "
            "and how to grow your wealth steadily — whether you are starting small "
            "or scaling up."
        ),
        "Ngozi Eze",
        "2025-04-25",
        "Apr 25, 2025",
        6,
    ),
    "stack": [
        card(
            "savings personal tips", "img/photos/laptop.jpg",
            "Budget chart on a laptop", "tag-green", "Savings",
            "7 Smart Ways to Save Money in Nigeria (Even on a Low Income)",
            "2025-04-22", "Apr 22, 2025", 7, "category:finance",
        ),
        card(
            "tips personal", "img/photos/team.jpg", "Experts discussing money",
            "tag-orange", "Personal Finance",
            "Understanding Inflation and How to Protect Your Money",
            "2025-04-20", "Apr 20, 2025", 5, "category:finance",
        ),
        card(
            "banking", "img/photos/city.jpg", "Bank building in the city",
            "tag-blue", "Banking",
            "The Best Nigerian Banks for Business Owners in 2025",
            "2025-04-17", "Apr 17, 2025", 6, "category:finance",
        ),
        card(
            "tips savings", "img/photos/cafe.jpg", "Saving money at a cafe",
            "tag-green", "Financial Tips",
            "Financial Freedom: 7 Habits of Successful Nigerians",
            "2025-04-15", "Apr 15, 2025", 8, "category:finance",
        ),
    ],
    "more": [
        card(
            "investing", "img/photos/crypto.jpg", "Digital assets",
            "tag-purple", "Investing",
            "Stocks vs. Crypto: Where Should Nigerians Invest in 2025?",
            "2025-04-12", "Apr 12, 2025", 7, "category:finance",
        ),
        card(
            "banking tips", "img/photos/founder.jpg",
            "Business owner reviewing finances", "tag-blue", "Banking",
            "Getting a Business Loan in Nigeria: What Banks Look For",
            "2025-04-10", "Apr 10, 2025", 6, "category:finance",
        ),
        card(
            "savings personal", "img/photos/ideas.jpg", "Written savings plan",
            "tag-green", "Savings",
            "A Simple Budget Template That Works for Nigerian Households",
            "2025-04-08", "Apr 8, 2025", 5, "category:finance",
        ),
    ],
    "cta": _subscribe_cta(
        "",
        _ICON_CHART,
        "Get smart with your money.",
        "Subscribe for the latest finance tips and business guides.",
    ),
}


CATEGORIES["business"] = {
    "nav_active": "business",
    "page_id": "business",
    "meta_title": "Business — News, strategies and growth ideas for Nigerian businesses",
    "meta_description": (
        "Business news, strategy, startups, small business and tools — practical "
        "resources for Nigerian entrepreneurs and business owners."
    ),
    "theme": "t-business",
    "image": "img/photos/city.jpg",
    "image_alt": "City skyline at dusk",
    "crumb": "Business",
    "heading": "Business",
    "blurb": (
        "Business news, market trends, growth strategies and tools for Nigerian "
        "entrepreneurs and business owners."
    ),
    "hero_actions": [
        link_cta("Browse Articles", "#latest"),
        link_cta("Startup Stories", "category:entrepreneur", "btn btn--outline-light"),
    ],
    "chips": [
        ("all", "All"),
        ("news", "Business News"),
        ("strategy", "Strategy"),
        ("startups", "Startups"),
        ("small", "Small Business"),
        ("tools", "Business Tools"),
    ],
    "feature": feature(
        "strategy small",
        "img/photos/laptop.jpg",
        "Laptop on a desk with growth charts",
        "Nigerian SMEs: 5 Strategies to Survive and Thrive in 2025",
        (
            "Discover practical strategies to help small and medium businesses "
            "navigate challenges, secure funding, and achieve sustainable growth."
        ),
        "Ngozi Eze",
        "2025-04-24",
        "Apr 24, 2025",
        6,
    ),
    "stack": [
        card(
            "strategy tools", "img/photos/ideas.jpg", "Notebook with a plan",
            "tag-blue", "Strategy", "How to Write a Winning Business Plan",
            "2025-04-21", "Apr 21, 2025", 6, "category:business",
        ),
        card(
            "news", "img/photos/phones.jpg", "Shopping on a phone",
            "tag-cyan", "Business News", "The Rise of E-commerce in Nigeria",
            "2025-04-18", "Apr 18, 2025", 4, "category:business",
        ),
        card(
            "small startups", "img/photos/team.jpg", "Founders meeting",
            "tag-orange", "Startups", "5 Nigerian Entrepreneurs Making Global Impact",
            "2025-04-16", "Apr 16, 2025", 7, "category:business",
        ),
        card(
            "strategy", "img/photos/city.jpg", "Growing business district",
            "tag-blue", "Small Business",
            "Business Opportunities in Nigeria’s Growing Sectors",
            "2025-04-15", "Apr 15, 2025", 8, "category:business",
        ),
    ],
    "more": [
        card(
            "tools", "img/photos/desk.jpg", "Bookkeeping desk",
            "tag-green", "Business Tools",
            "7 Free Tools Every Nigerian Small Business Needs",
            "2025-04-13", "Apr 13, 2025", 6, "category:business",
        ),
        card(
            "news strategy", "img/photos/founder.jpg",
            "Entrepreneur reviewing results", "tag-blue", "Business News",
            "What Nigeria’s New Tax Act Means for Your Business",
            "2025-04-11", "Apr 11, 2025", 5, "category:business",
        ),
        card(
            "startups", "img/photos/startup.jpg", "Founder on a ridge",
            "tag-orange", "Startups",
            "How to Register a Company in Nigeria: A Step-by-Step Guide",
            "2025-04-09", "Apr 9, 2025", 7, "category:business",
        ),
    ],
    "cta": _link_band(
        "cta--blue",
        _ICON_BARS,
        "Grow Your Business",
        "Get expert insights, tools and resources to scale your business.",
        "Explore Resources",
        "category:business",
    ),
}



CATEGORIES["crypto"] = {
    "nav_active": "crypto",
    "page_id": "crypto",
    "meta_title": "Crypto / Web 3.0 — Blockchain news and opportunities",
    "meta_description": (
        "Blockchain, crypto news, Web3, DeFi and NFT insights for Nigerians — the "
        "next generation of on-chain business and investment."
    ),
    "theme": "t-crypto",
    "image": "img/photos/crypto.jpg",
    "image_alt": "Crypto coins with a blockchain network",
    "crumb": "Crypto / Web 3.0",
    "heading": "Crypto / Web 3.0",
    "blurb": (
        "Blockchain, crypto news, Web3 innovations and opportunities for the "
        "next generation."
    ),
    "hero_actions": [
        link_cta("Read the Latest", "#latest"),
        link_cta("Investing Basics", "category:finance", "btn btn--outline-light"),
    ],
    "chips": [
        ("all", "All"),
        ("crypto", "Crypto News"),
        ("web3", "Web3"),
        ("blockchain", "Blockchain"),
        ("defi", "DeFi"),
        ("nfts", "NFTs"),
    ],
    "feature": feature(
        "crypto blockchain",
        "img/photos/crypto.jpg",
        "Bitcoin and altcoins",
        "Bitcoin Price Analysis: What to Expect in 2025",
        (
            "A deep dive into Bitcoin’s price trends, market sentiment and "
            "investment outlook — what experienced traders and analysts expect "
            "for the rest of the year."
        ),
        "Chinedu Okafor",
        "2025-04-23",
        "Apr 23, 2025",
        7,
    ),
    "stack": [
        card(
            "crypto", "img/photos/crypto.jpg", "Altcoin list",
            "tag-purple", "Crypto News", "Top 5 Altcoins to Watch in 2025",
            "2025-04-20", "Apr 20, 2025", 5, "category:crypto",
        ),
        card(
            "web3", "img/photos/phones.jpg", "Web3 apps on a phone",
            "tag-cyan", "Web3", "What is Web3 and Why It Matters",
            "2025-04-18", "Apr 18, 2025", 6, "category:crypto",
        ),
        card(
            "defi", "img/photos/coins.jpg", "DeFi tokens",
            "tag-green", "DeFi", "How to Get Started with DeFi",
            "2025-04-16", "Apr 16, 2025", 6, "category:crypto",
        ),
        card(
            "crypto blockchain", "img/photos/desk.jpg",
            "Crypto wallet checklist", "tag-purple", "Wallets",
            "Best Crypto Wallets for Nigerians",
            "2025-04-14", "Apr 14, 2025", 5, "category:crypto",
        ),
    ],
    "more": [
        card(
            "nfts", "img/photos/team.jpg", "Digital collectables",
            "tag-orange", "NFTs",
            "NFTs in Nigeria: Creative Passions Meet Blockchain",
            "2025-04-12", "Apr 12, 2025", 6, "category:crypto",
        ),
        card(
            "blockchain web3", "img/photos/city.jpg",
            "Distributed network over a city", "tag-blue", "Blockchain",
            "Beyond Crypto: Real-World Use Cases of Blockchain in Nigeria",
            "2025-04-10", "Apr 10, 2025", 8, "category:crypto",
        ),
        card(
            "defi crypto", "img/photos/founder.jpg", "Person using a crypto app",
            "tag-green", "DeFi", "Yield Farming Explained for First-Time Users",
            "2025-04-07", "Apr 7, 2025", 7, "category:crypto",
        ),
    ],
    "cta": _subscribe_cta(
        "cta--purple",
        _ICON_CLOCK,
        "Stay Ahead in Web3",
        "Get the latest crypto news, Web3 updates and opportunities.",
    ),
}



CATEGORIES["entrepreneur"] = {
    "nav_active": "entrepreneur",
    "page_id": "startup",
    "meta_title": "Entrepreneur Corner — Inspiration, skills and funding",
    "meta_description": (
        "Inspiration, startup stories, skills, tools and resources for aspiring "
        "and existing Nigerian entrepreneurs — from idea to impact."
    ),
    "theme": "t-startup",
    "image": "img/photos/startup.jpg",
    "image_alt": "Entrepreneur silhouette on a mountain ridge at sunrise",
    "crumb": "Entrepreneur Corner",
    "heading": "Entrepreneur Corner",
    "blurb": (
        "Inspiration, startup stories, skills, tools and resources for aspiring "
        "and existing entrepreneurs."
    ),
    "hero_actions": [
        link_cta("Browse Articles", "#latest"),
        link_cta("Free Resources", "page:services", "btn btn--outline-light"),
    ],
    "chips": [
        ("all", "All"),
        ("startups", "Startups"),
        ("stories", "Startup Stories"),
        ("skills", "Skills & Tools"),
        ("funding", "Funding"),
        ("motivation", "Motivation"),
    ],
    "feature": feature(
        "motivation stories",
        "img/photos/founder.jpg",
        "Founder smiling with a laptop",
        "From Idea to Impact: Lessons from Nigerian Founders",
        (
            "Real stories from entrepreneurs who turned small ideas into "
            "successful businesses — the setbacks, the strategies and the "
            "lessons they learned."
        ),
        "Ngozi Eze",
        "2025-04-19",
        "Apr 19, 2025",
        8,
    ),
    "stack": [
        card(
            "startups skills", "img/photos/ideas.jpg",
            "Testing a business idea", "tag-orange", "Startups",
            "How to Validate Your Business Idea",
            "2025-04-15", "Apr 15, 2025", 6, "category:entrepreneur",
        ),
        card(
            "skills", "img/photos/team.jpg", "Team working together",
            "tag-blue", "Skills & Tools", "Essential Skills Every Entrepreneur Needs",
            "2025-04-12", "Apr 12, 2025", 7, "category:entrepreneur",
        ),
        card(
            "funding", "img/photos/city.jpg", "Investors meeting",
            "tag-cyan", "Funding", "Accessing Funding as a Nigerian Startup",
            "2025-04-10", "Apr 10, 2025", 6, "category:entrepreneur",
        ),
        card(
            "motivation", "img/photos/startup.jpg",
            "Climbing the next mountain", "tag-orange", "Motivation",
            "Overcoming Challenges as a Young Entrepreneur",
            "2025-04-08", "Apr 8, 2025", 6, "category:entrepreneur",
        ),
    ],
    "more": [
        card(
            "stories", "img/photos/laptop.jpg", "Founder at work",
            "tag-green", "Startup Stories",
            "How a Lagos Side Hustle Became a ₦50M Yearly Business",
            "2025-04-06", "Apr 6, 2025", 7, "category:entrepreneur",
        ),
        card(
            "funding startups", "img/photos/cafe.jpg",
            "Pitch meeting over coffee", "tag-blue", "Funding",
            "Grants and Programs Nigerian Founders Can Apply For",
            "2025-04-04", "Apr 4, 2025", 8, "category:entrepreneur",
        ),
        card(
            "skills tools", "img/photos/desk.jpg", "Planning a launch",
            "tag-purple", "Skills & Tools",
            "Project Management Basics for Busy Founders",
            "2025-04-02", "Apr 2, 2025", 6, "category:entrepreneur",
        ),
    ],
    "cta": _link_band(
        "cta--orange",
        _ICON_BOLT,
        "Turn Your Idea Into a Business",
        "Get resources, mentorship and tools to help you grow.",
        "Explore More",
        "page:contact",
    ),
}



CATEGORIES["affiliates"] = {
    "nav_active": "affiliate",
    "page_id": "affiliates",
    "meta_title": "Affiliates — Make money online with affiliate marketing",
    "meta_description": (
        "Affiliate marketing, online income, programs and proven strategies — "
        "learn how to make money online in Nigeria as an affiliate marketer."
    ),
    "theme": "t-affiliate",
    "image": "img/photos/phones.jpg",
    "image_alt": "Hand holding a phone showing an affiliate dashboard",
    "crumb": "Affiliates",
    "heading": "Affiliates",
    "blurb": (
        "Make money online, affiliate programs, and digital opportunities — "
        "join our growing community of smart earners."
    ),
    "hero_actions": [
        link_cta("Browse Articles", "#latest"),
        link_cta("Join the Community", "page:contact", "btn btn--outline-light"),
    ],
    "chips": [
        ("all", "All"),
        ("marketing", "Affiliate Marketing"),
        ("online", "Online Income"),
        ("programs", "Programs"),
        ("guides", "Tips & Guides"),
    ],
    "feature": feature(
        "marketing guides",
        "img/photos/phones.jpg",
        "Affiliate dashboard on a smartphone",
        "Step-by-Step Guide to Making Money with Affiliate Marketing in Nigeria",
        (
            "Step-by-step tutorial on getting started and earning online — "
            "practical strategies for building traffic and converting clicks "
            "into income."
        ),
        "Ngozi Eze",
        "2025-04-18",
        "Apr 18, 2025",
        10,
    ),
    "stack": [
        card(
            "programs", "img/photos/crypto.jpg", "Program list",
            "tag-purple", "Programs", "Top 10 Best Affiliate Programs for Nigerians",
            "2025-04-16", "Apr 16, 2025", 7, "category:affiliates",
        ),
        card(
            "marketing guides", "img/photos/laptop.jpg", "Blog being written",
            "tag-green", "Tips & Guides", "How to Create a High-Converting Blog",
            "2025-04-14", "Apr 14, 2025", 8, "category:affiliates",
        ),
        card(
            "online", "img/photos/coins.jpg", "Passive income coins",
            "tag-blue", "Online Income", "Passive Income Ideas for 2025",
            "2025-04-12", "Apr 12, 2025", 6, "category:affiliates",
        ),
        card(
            "marketing", "img/photos/team.jpg", "Marketing meeting",
            "tag-orange", "Affiliate Marketing",
            "Affiliate Marketing Mistakes to Avoid",
            "2025-04-10", "Apr 10, 2025", 6, "category:affiliates",
        ),
    ],
    "more": [
        card(
            "online", "img/photos/ideas.jpg", "Digital product ideas",
            "tag-cyan", "Online Income",
            "Selling Digital Products in Nigeria: A Beginner’s Roadmap",
            "2025-04-08", "Apr 8, 2025", 7, "category:affiliates",
        ),
        card(
            "guides", "img/photos/founder.jpg", "Creator with a camera",
            "tag-blue", "Tips & Guides",
            "Using Short-Form Video to Drive Affiliate Sales",
            "2025-04-06", "Apr 6, 2025", 6, "category:affiliates",
        ),
        card(
            "programs online", "img/photos/city.jpg",
            "Global affiliate network", "tag-green", "Programs",
            "How Affiliate Payments Work: Payout Methods Nigerians Can Use",
            "2025-04-03", "Apr 3, 2025", 5, "category:affiliates",
        ),
    ],
    "cta": _link_band(
        "cta--cyan",
        _ICON_SHARE,
        "Start Earning Online",
        "Join 50+ affiliate programs and earn with proven strategies.",
        "Get Started",
        "page:contact",
    ),
}


# Static (non-category) pages: slug -> template.
STATIC_PAGES = {
    "services": "pages/services.html",
    "about": "pages/about.html",
    "contact": "pages/contact.html",
    "privacy-policy": "pages/privacy_policy.html",
    "terms-of-service": "pages/terms_of_service.html",
    "cookies": "pages/cookies.html",
}

# Long-form articles: slug -> template.
ARTICLES = {
    "10-profitable-business-ideas": "pages/article.html",
}


