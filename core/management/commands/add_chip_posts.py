"""Give every category filter chip at least fifteen published articles.

Category pages render up to fifteen articles per filter chip
(/category/<slug>/?filter=<chip>). Earlier seeding passes spread a handful
of posts across each category's chips, which left several filters empty or
far below fifteen.

Idempotent: titles that already exist are skipped, so it is safe to re-run.
Prints a per-chip report at the end so any shortfall is obvious.
"""
import re
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from core import content
from core.models import Post
from core.management.commands.replace_posts_with_editorial import IMAGES, article_body

TARGET_PER_CHIP = 15

# (category, title, tags, excerpt) — tags mirror the filter chips of the
# category, two or three per post, so every chip clears the target.
POSTS = [
    # ---- finance ----
    ("finance", "How to Build an Emergency Fund on an Irregular Income", "savings banking", "A simple buffer rule for freelancers and business owners whose revenue refuses to behave."),
    ("finance", "Fixed Deposits vs Treasury Bills: Where to Park Cash This Year", "investing banking", "Rates, lock-up periods, safety and access — compared for savers who want predictability."),
    ("finance", "The 50/30/20 Budget Rule, Tuned for Nigerian Salaries", "personal savings", "Needs, wants and savings shares you can adjust when prices move faster than your pay."),
    ("finance", "Reading Your Bank's Hidden Charges: A Consumer Checklist", "banking personal tips", "Transfer fees, SMS levies and maintenance costs decoded — and how to push back on them."),
    ("finance", "How to Start Investing in Nigeria With ₦10,000", "investing tips", "Small-ticket options that let beginners learn the market without risking serious money."),
    ("finance", "Index Funds Explained: Low-Cost Investing for Beginners", "investing personal", "Why buying the whole market beats picking winners for most people — and how to begin."),
    ("finance", "How Much Cash Should You Keep? A Liquidity Rule of Thumb", "investing savings", "A practical formula for money that must stay reachable versus money that should work."),
    ("finance", "Investing in US Stocks From Nigeria: The Practical Path", "investing tips banking", "Broker choice, funding, taxes and currency risk — the steps that actually work locally."),
    ("finance", "How to Talk About Money With Your Partner", "personal tips", "Scripts and rules for the conversation most couples keep avoiding until it gets urgent."),
    ("finance", "Surviving Inflation: Seven Habits That Actually Help", "personal savings tips", "Buying patterns, debt hygiene and buffer-building that protect household budgets."),
    ("finance", "Salary Not Enough? A Practical Side-Income Framework", "personal", "Pick one skill, price it honestly, and grow it without quitting your day job."),
    ("finance", "How to Negotiate a Raise With Numbers, Not Feelings", "personal tips", "Document impact, anchor the range, and handle the silence after you make your ask."),
    ("finance", "Talking to Your Children About Money Before They Turn Ten", "personal", "Allowance systems, patience and visible saving that build money habits early."),
    ("finance", "The Real Cost of Owning a Car in Lagos", "personal banking", "Fuel, insurance, repairs, parking and depreciation — the full maths before you buy."),
    ("finance", "How to File Taxes as a Freelancer in Nigeria", "personal banking tips", "Registrations, records and deadlines for self-employed earners who hate paperwork."),
    ("finance", "Retirement at 50 or 60? The Power of Starting Early", "investing personal savings", "Compound interest forgives many sins — but only if you give it enough years."),
    ("finance", "Why Your Budget Fails by the 20th of the Month", "personal savings tips", "The structural mistakes that break monthly plans and the fixes that survive payday."),
    ("finance", "How to Protect Your Credit Score With Nigerian Banks", "personal banking", "What lenders check, how defaults are recorded, and how to repair a damaged score."),
    ("finance", "Money Mindset Shifts That Free Up Cash Every Month", "personal tips", "Small belief changes that make saving automatic instead of heroic."),
    ("finance", "High-Yield Savings Accounts in Nigeria, Compared", "savings banking", "Returns, withdrawal rules and deposit insurance across the accounts worth considering."),
    ("finance", "The Bi-Weekly Savings Challenge That Actually Works", "savings tips", "An escalating deposit plan you can keep up even when the month turns hostile."),
    ("finance", "How to Save for School Fees Without Panic Saving", "savings personal", "Twelve-month planning for education costs that arrive like clockwork."),
    ("finance", "Automate Your Savings Before You Spend a Dime", "savings banking tips", "Standing orders and salary-day transfers that remove willpower from the equation."),
    ("finance", "How to Choose a Current Account That Serves Your Business", "banking tips", "Settlement times, charge schedules and support quality compared across providers."),
    ("finance", "Domiciliary Accounts Explained: Types, Rules and Costs", "banking personal", "Opening requirements, maintenance fees and usage limits for dollar, pound and euro accounts."),
    ("finance", "When the CBN Changes Rates: What Savers Should Do Next", "investing banking", "A calm response plan for depositors when monetary policy shifts mid-year."),
    ("finance", "How to Evaluate Agric Investment Schemes Without Getting Scammed", "investing personal tips", "Promises, operators and due diligence questions that separate real returns from fraud."),
    ("finance", "How to Pick a Broker: Seven Checks Before You Fund an Account", "investing tips banking", "Regulation, fees, platform stability and withdrawal speed that separate brokers from risk."),
    ("finance", "Building Wealth Slowly: The Case for Patient Investors", "investing savings tips", "Why boring consistency beats chasing every hot market — with the maths to prove it."),
    # ---- business ----
    ("business", "Fuel Price Changes and What They Mean for Small Businesses", "news small", "Haulage, pricing and delivery promises — adjusting when energy costs jump overnight."),
    ("business", "CBN Policy Briefing: What the Latest Moves Mean for Founders", "news strategy", "Interest rates, the naira and credit — a plain-English read for people who run companies."),
    ("business", "Nigeria's Company Registration Portal: What Changed for New Filings", "news tools", "Faster incorporation is real — here is what to prepare before you start the form."),
    ("business", "Lagos State Raises Levies Again — How SMEs Should Respond", "news small", "Budgeting for permit season and challenging charges that do not apply to you."),
    ("business", "Funding Cooled Last Quarter — Where the Money Actually Went", "news startups", "Fewer, larger rounds: what investors are rewarding in the current climate."),
    ("business", "How to Price Without Losing Customers in an Inflationary Market", "strategy small", "Phased increases, smaller packs and anchoring tricks that soften the shock."),
    ("business", "Choosing Your Business Structure: Sole Proprietorship, LLC or Partnership", "strategy startups", "Liability, taxes and investor readiness compared for first-time registrants."),
    ("business", "Turnaround Mode: The 12-Week Plan for a Bleeding Business", "strategy small", "Cut, protect and fix — the order matters more than the courage."),
    ("business", "Build a One-Page Business Plan You'll Actually Use", "strategy tools", "One page, five boxes, one metric per goal — planning that survives contact with reality."),
    ("business", "Competing on Speed: Why Fast Operators Win in Nigerian Markets", "strategy small", "Quote within the hour, deliver within the day — the service edge money cannot copy easily."),
    ("business", "The Three Costs That Quietly Kill Early-Stage Startups", "startups small", "Office rent, premature hires and discounting — where runway disappears first."),
    ("business", "Bootstrapping in Lagos: Founders Share What Actually Worked", "startups small", "Revenue-first stories from operators who never took an investor's money."),
    ("business", "Pivoting Without Panic: Signs Your Model Needs a Change", "startups strategy", "Retention, margins and repeated objections — the signals that justify a switch."),
    ("business", "The Founder's Legal Checklist Before Raising Money", "startups tools", "Cap tables, contracts and IP assignment — paperwork investors will ask for anyway."),
    ("business", "Hiring Your First Employee: Contracts, Probation and Payroll", "startups small", "What the law requires, what to put in writing, and how to part ways cleanly if needed."),
    ("business", "Inventory Tracking for Small Shops: From Exercise Book to App", "small tools", "A staged upgrade path that never breaks your counting rhythm."),
    ("business", "Cutting Costs Without Cutting Quality: A Practical Audit", "small strategy", "Where to trim first, and the corners customers will notice immediately."),
    ("business", "WhatsApp Business as a Storefront: A Setup Guide", "small tools", "Catalogues, quick replies and labels that turn chats into a sales pipeline."),
    ("business", "PoS Operators and the New CBN Rules: What Operators Must Fix", "small news", "Compliance deadlines, KYC tiers and the transactions most likely to be affected."),
    ("business", "Five Free Tools That Run a Small Team", "tools strategy", "Scheduling, invoicing, files and chat — a lean stack that costs nothing to start."),
    ("business", "Choosing an Accounting App: Spreadsheets, QuickBooks or Zoho?", "tools small", "Features, price and learning curve compared for micro and small businesses."),
    ("business", "Setting Up Business Email and a Domain That Builds Trust", "tools small", "A cheap domain, proper DNS and the mailbox setup clients take seriously."),
    ("business", "Automation for One-Person Businesses: Where to Start", "tools strategy", "Automate the repetitive three before you buy another subscription."),
    ("business", "Oil Prices, the Naira and Your Annual Business Budget", "news strategy", "Scenario planning for founders whose costs are dollar-linked but sales are not."),
    ("business", "Nigeria's Startup Act One Year On: Wins and Gaps", "news startups", "Incentives delivered, promises pending — what founders should actually use."),
    ("business", "Pitch Decks That Got Nigerian Founders Funded", "startups tools", "Twelve slides, one story, and the numbers investors kept asking to see."),
    ("business", "How Small Retailers Survive the December Squeeze", "small", "Stock discipline, pre-orders and cash timing for the busiest, tightest month."),
    ("business", "Electricity Tariffs Explained for Business Owners", "news", "Band changes, meter options and generator maths in plain terms."),
    ("business", "New Lagos Waste Fees: What Shop Owners Must Know", "news small", "Who collects, how much, and the paperwork that prevents double payment."),
    ("business", "Bank Charges Review: What the Latest Directive Means", "news tools", "Transfer limits, PoS fees and the complaints channel that actually works."),
    ("business", "Two Nigerian Startups Raise Fresh Funding — Lessons Inside", "news startups", "What the announced rounds reveal about investor appetite right now."),
    # ---- crypto ----
    ("crypto", "Stablecoins Are Nigeria's Busiest Crypto Product — Here's Why", "crypto defi", "Dollar exposure, diaspora transfers and merchant payments keep demand steady."),
    ("crypto", "Bitcoin Steadies as Institutional Desks Warm to Africa", "crypto web3", "Flows, halving cycles and what the latest positioning means for retail holders."),
    ("crypto", "What Blockchain Actually Does: A Non-Tech Founder's Guide", "blockchain", "Shared records, immutability and where the technology genuinely beats a spreadsheet."),
    ("crypto", "Lending, Borrowing and Yield: DeFi in Plain English", "defi blockchain", "How smart contracts replace the middleman — and what happens when they glitch."),
    ("crypto", "How Liquidity Pools Work (and Where Retail Traders Get Hurt)", "defi", "Impermanent loss, slippage and fees explained with one realistic example."),
    ("crypto", "Choosing a DeFi Wallet: Non-Custodial Basics and Backup Rules", "defi crypto", "Seed phrases, hardware pairing and the recovery drill everyone postpones."),
    ("crypto", "NFTs Beyond Jpegs: Ticketing, Membership and Real Utility", "nfts web3", "The projects that survived by solving access, identity and loyalty problems."),
    ("crypto", "How NFT Marketplaces Detect and Flag Scam Collections", "nfts blockchain", "Verification signals, metadata checks and the red flags traders can spot early."),
    ("crypto", "Creator Royalties: How Smart Contracts Enforce Them", "nfts defi", "Why secondary sales can keep paying creators — and where royalties still break."),
    ("crypto", "Decentralised Identity: Why Your Wallet May Become Your Passport", "web3 blockchain", "Verifiable credentials without a central database — plus the privacy trade-offs."),
    ("crypto", "DAOs Explained: Governing a Company With Tokens", "web3 blockchain", "Proposals, treasuries and voting — how token communities actually decide."),
    ("crypto", "Gaming and Web3: Play-to-Earn After the Hype", "web3 nfts", "What remains when speculation leaves: ownership, skins and player-driven economies."),
    ("crypto", "Rug Pulls: Red Flags Before You Send Funds", "defi blockchain", "Unlocked liquidity, anonymous teams and honeypot contracts that trap sellers."),
    ("crypto", "Staking Explained: Rewards, Lock-ups and Slashing Risks", "defi crypto", "Consensus participation as passive income — with the failure modes priced in."),
    ("crypto", "Regulation Watch: Nigeria's Digital Asset Rules Explained", "crypto web3", "What is permitted, what is restricted and what operators should document now."),
    ("crypto", "Layer 2s: Why Cheaper Transactions Matter for African Users", "blockchain crypto", "Rollups, fees and the UX improvements that finally make on-chain viable."),
    ("crypto", "Tokenising Music: What Nigerian Creators Should Know", "nfts web3", "Royalty splits, licensing and the platforms experimenting with fan ownership."),
    ("crypto", "Digital Art in Lagos: Where On-Chain Meets Off-Chain", "nfts web3", "Galleries bridging physical exhibitions with verifiable digital provenance."),
    ("crypto", "Cross-Border Payments With Stablecoins: A Practical Test", "defi crypto", "We sent money between Lagos and Nairobi and measured cost, speed and friction."),
    ("crypto", "Public vs Private Blockchains: Which Uses Make Sense", "blockchain web3", "Permissionless openness versus controlled records — choosing for real business needs."),
    ("crypto", "Yield Farming After the Boom: The Sober Math", "defi blockchain", "Where sustainable returns still exist, and how to stress-test an APY."),
    ("crypto", "How Event Organisers Are Using NFT Tickets", "nfts blockchain", "Anti-scalping, resale control and VIP access via verifiable tickets."),
    ("crypto", "P2P Trading Safety: Escrow, Ratings and Red Flags", "crypto defi", "Habits that keep counterparties honest on peer-to-peer platforms."),
    ("crypto", "Oracles: The Bridge Between Blockchains and Real Data", "web3 defi", "Why a smart contract needs outside information — and how manipulation happens."),
    ("crypto", "Token Standards Explained: ERC-20, ERC-721 and Beyond", "blockchain web3", "What the standards decide about transfer rules, royalties and compatibility."),
    ("crypto", "Memecoins and Mania: How Traders Spot the Top", "crypto nfts", "Social volume, holder concentration and the exit-liquidity warning signs."),
    ("crypto", "Interoperability: Moving Assets Across Chains Safely", "web3 blockchain", "Bridges, wrapped assets and the checks to run before you transfer."),
    ("crypto", "Bridges Explained: How Assets Move Between Networks", "defi blockchain", "Lock-and-mint versus burn-and-mint — and why bridges get hacked."),
    ("crypto", "What Is TVL and Why Traders Watch It", "defi crypto", "Total value locked as a health signal — and the ways it can be gamed."),
    ("crypto", "Perps and Futures DEXs: Leverage Without a Centralised Exchange", "defi blockchain", "Funding rates, liquidations and the risks of on-chain leverage."),
    ("crypto", "Yield Aggregators: Automating DeFi Positions", "defi web3", "Vault strategies that compound returns — plus the contract risk they hide."),
    ("crypto", "Token Swaps: Slippage, Routes and Gas Explained", "defi crypto", "Why your swap costs more than the quoted price, and how to route smarter."),
    ("crypto", "NFT Lending: Borrowing Against Digital Collectibles", "nfts defi", "Collateral ratios, floor-price risk and liquidation timelines."),
    ("crypto", "Digital Fashion: Wearables for the Metaverse Economy", "nfts web3", "Brands selling identity, not fabric — and the resale markets it created."),
    ("crypto", "Dynamic NFTs: Collectibles That Evolve Over Time", "nfts blockchain", "Tokens that change with achievements, seasons or real-world events."),
    ("crypto", "Ordinals and Bitcoin NFTs: The New Collectible Layer", "nfts crypto", "Inscriptions, block-space fees and culture on the oldest chain."),
    ("crypto", "Community Tokens: When Fandom Becomes Ownership", "nfts web3", "Social tokens, gated perks and the fine print of community economies."),
    ("crypto", "Protecting Yourself From Fake NFT Listings", "nfts blockchain", "Contract checks and marketplace hygiene that prevent one-click mistakes."),
    # ---- entrepreneur ----
    ("entrepreneur", "From Jollof Cart to Catering Company: Grace's Playbook", "stories skills", "How one cook systematised orders, staff and delivery until the business could grow without her."),
    ("entrepreneur", "How Three Friends Turned ₦50,000 into a Printing Business", "stories funding", "Split roles, reinvested profits and the handshake agreement that held for six years."),
    ("entrepreneur", "I Folded My First Startup at 27 — What I'd Do Differently", "stories motivation", "A candid post-mortem on runway, co-founders and the warning signs ignored."),
    ("entrepreneur", "The Kano Textile Brand That Now Exports to Four Countries", "stories startups", "Quality control, trade fairs and distributor trust as the growth engine."),
    ("entrepreneur", "From Classroom to Content Studio: A Teacher's Second Act", "stories motivation", "Turning lesson-planning skills into a media business that pays consistently."),
    ("entrepreneur", "Revenue First: How Founders Fund Growth From Sales", "funding startups", "Why earning before raising keeps options open — and when debt still makes sense."),
    ("entrepreneur", "Writing Grants That Get Funded: A Step-by-Step Guide", "funding skills", "Problem, evidence, budget and sustainability — the structure funders reward."),
    ("entrepreneur", "Angel Investors in Lagos: Where to Find Them and What They Ask", "funding startups", "Demo days, warm intros and the diligence questions that separate serious money."),
    ("entrepreneur", "Rejected Again: How to Pitch After a No", "funding motivation stories", "Treating rejection as data — and the follow-up that eventually opened the door."),
    ("entrepreneur", "Bank Loans vs Microfinance: What a Small Borrower Actually Pays", "funding stories startups", "Effective rates, collateral and hidden fees compared with a real case."),
    ("entrepreneur", "Sales Calls Without Cringe: A Script for Shy Founders", "skills startups", "Openings, discovery questions and exits that feel like conversations, not pitches."),
    ("entrepreneur", "Networking That Actually Works: Getting the Intros You Need", "skills motivation", "Give first, follow up fast, and make it easy for people to champion you."),
    ("entrepreneur", "Financial Modelling for Non-Finance Founders", "skills funding startups", "Build a three-tab model that answers investors' real questions."),
    ("entrepreneur", "Hiring Your First Team Without Burning Cash", "skills startups", "Roles, trials and pay structures that protect both sides early."),
    ("entrepreneur", "Scope Creep: Taming Revisions Without Losing Clients", "skills stories", "Contracts, change orders and phrasing that keeps relationships intact."),
    ("entrepreneur", "Feedback That Doesn't Sting: Managing With Kindness", "skills motivation", "Situation, impact, ask — the framework that makes correction safe."),
    ("entrepreneur", "Discipline Over Motivation: The Founder's Daily Routine", "motivation startups", "Why systems beat mood, and a template day that ships work consistently."),
    ("entrepreneur", "Comparison Is Killing Your Consistency", "motivation skills", "Measuring your chapter three against someone else's chapter ten."),
    ("entrepreneur", "The Rejection Stack: Every 'No' Behind One 'Yes'", "motivation stories", "Counting the nos that preceded the deal changed how rejection feels."),
    ("entrepreneur", "Keeping Faith When the Runway Shrinks", "motivation funding", "Decision rules for founders facing hard months without clear answers."),
    ("entrepreneur", "Lagos vs Abuja vs PH: Where to Register and Why", "startups stories", "Costs, ecosystems and market access compared for new businesses."),
    ("entrepreneur", "Customer Interviews That Don't Waste Anyone's Time", "startups skills", "Seven questions that surface real problems instead of polite compliments."),
    ("entrepreneur", "Quitting Your Job to Build: A Sober Checklist", "startups motivation", "Savings runway, household buy-in and exit timing before you hand in the letter."),
    ("entrepreneur", "CAC Registration Costs, Explained for New Founders", "funding startups", "Name reservation to certificates — the fees and timelines at each step."),
    ("entrepreneur", "Pricing Your Service So You Can Pay Yourself", "skills funding", "Cost-plus, value-based and hybrid models with a rate-card exercise."),
    ("entrepreneur", "From Sewing Machine to Fashion Label: Amaka's Numbers", "stories funding", "Unit economics, wholesale breaks and the season that made the business."),
    ("entrepreneur", "A Simple Cash-Flow Forecast for Small Teams", "funding skills", "Thirteen-week visibility that prevents the surprises that sink healthy businesses."),
    ("entrepreneur", "The Mentor Who Changed My Pricing", "motivation stories", "One sentence in a busy room reframed what the work was worth."),
    # ---- affiliates ----
    ("affiliates", "Choosing Your First Affiliate Program: Six Honest Filters", "marketing guides", "Commission structure, cookie window, product fit and payout reality — before you commit."),
    ("affiliates", "Content That Sells: Writing Reviews People Actually Trust", "marketing online", "Structure, disclosure and lived experience that turn readers into buyers."),
    ("affiliates", "SEO for Affiliate Sites: What Still Works After Every Update", "marketing guides", "Intent-matching, honest comparisons and internal links that keep ranking."),
    ("affiliates", "Amazon Associates vs Jumia KOL: A Nigerian Creator's Comparison", "programs marketing", "Rates, thresholds and product availability compared for local traffic."),
    ("affiliates", "Recurring Commissions: Programs That Keep Paying Monthly", "programs online", "SaaS and subscription offers where one reader can pay you for a year."),
    ("affiliates", "How to Read an Affiliate Program's Terms Before You Sign Up", "programs guides", "The clauses that quietly void commissions — and the ones worth negotiating."),
    ("affiliates", "Link Placement Matters: Where Clicks Actually Come From", "guides online", "In-content, comparison tables and call-to-action positions measured over a year."),
    ("affiliates", "Disclosure Done Right: Staying Legal and Trustworthy", "guides marketing", "What regulators expect and how honest disclosure can raise, not lower, clicks."),
    ("affiliates", "Building an Email List That Buys From You Repeatedly", "online guides", "Lead magnets, welcome sequences and the two emails that earn the most."),
    ("affiliates", "Pinterest Traffic for Nigerian Creators: A Starter Plan", "online marketing", "Boards, pins and scheduling habits that send steady buyer intent."),
    ("affiliates", "YouTube Product Tutorials That Convert Viewers", "online guides", "Demo structure, honest cons and description links that get clicked."),
    ("affiliates", "Recurring SaaS Programs Worth Promoting This Season", "programs marketing", "What to look for in dashboards, cookies and support before recommending tools."),
    ("affiliates", "Cookie Windows Explained: Why Your Sale Didn't Track", "programs guides", "Attribution rules, cross-device gaps and how to document disputes."),
    ("affiliates", "Paid Ads for Affiliates: When the Maths Actually Works", "marketing online", "EPC against cost-per-click — the only calculation that matters before scaling."),
    ("affiliates", "Product Demo Videos: A Simple Recipe That Sells", "guides online", "Hook, problem, proof and call to action in under five minutes."),
    ("affiliates", "From ClickBank to Expertnaira: Comparing Payout Thresholds", "programs marketing", "Minimums, methods and delays for creators cashing out in Nigeria."),
    ("affiliates", "Updating Old Posts: The Quickest Ranking Win", "guides marketing", "Refresh dates, better examples and internal links that revive stale traffic."),
    ("affiliates", "Niche Selection: Finding an Audience With Wallets", "online guides", "Demand, competition and your own credibility — the three-way overlap."),
    ("affiliates", "Analytics for Affiliates: The Four Numbers That Matter", "marketing guides", "Clicks, conversion, EPC and refund rate — read weekly, act monthly."),
    ("affiliates", "Telegram Communities as a Distribution Channel", "online marketing", "Group value first, offers second — building a list you actually own."),
    ("affiliates", "Payout Methods for Nigerians: Bank, PayPal and Crypto Rails", "programs online", "Fees, limits and workarounds for getting paid without losing a slice."),
    ("affiliates", "Questions to Ask Before Joining Any Program", "programs guides", "A pre-signup checklist that saves you from hidden clauses and dead dashboards."),
    ("affiliates", "Turning Program Dashboards Into Weekly Reviews", "programs marketing", "A thirty-minute routine that shows which promotions deserve more effort."),
    # ---- top-ups: business/startups + affiliates/programs ----
    ("business", "Startup Accelerators in Nigeria: What You Actually Get", "startups strategy", "Cohorts, demo days and equity terms — evaluating whether an accelerator fits your stage."),
    ("business", "The Co-founder Conversation Nobody Wants to Have", "startups tools", "Equity splits, roles and exit terms to agree before the first customer, not after."),
    ("business", "When to Build an Advisory Board (And Who to Ask)", "startups strategy", "Compensation, commitment and the gaps an advisor should realistically fill."),
    ("affiliates", "Program Dashboards Compared: Reporting You Can Trust", "programs guides", "Attribution transparency, export options and support response times across networks."),
    ("affiliates", "Promoting Programs During Peak Shopping Season", "programs marketing", "Planning content around festive spikes without spamming your readers."),
    ("affiliates", "Negotiating Higher Commissions Once You Have Volume", "programs online", "Traffic evidence, exclusivity and the script that turns flat rates into better splits."),
]


class Command(BaseCommand):
    help = "Give every category filter chip at least 15 published articles."

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
                published_at=now - timedelta(minutes=11 * (index + 1)),
            )
            created += 1
        self.stdout.write(self.style.SUCCESS(f"Created {created} new posts."))

        # Per-chip report — every chip on every category page needs 15+.
        shortfall = False
        for slug, label in Post.CATEGORY_CHOICES:
            chips = [
                value
                for value, _ in content.CATEGORIES.get(slug, {}).get("chips", [])
                if value != "all"
            ]
            posts = list(Post.published().filter(category=slug))
            for value in chips:
                count = sum(
                    1
                    for post in posts
                    if value in set(re.split(r"[ ,]+", post.tags.lower()))
                )
                line = f"{label} / {value}: {count} posts"
                if count < TARGET_PER_CHIP:
                    shortfall = True
                    self.stderr.write(self.style.WARNING(f"{line} — below 15!"))
                else:
                    self.stdout.write(line)
        if shortfall:
            self.stderr.write(self.style.WARNING("Some chips are still short — re-run after adding more."))
        else:
            self.stdout.write(self.style.SUCCESS("Every filter chip has 15+ posts."))
