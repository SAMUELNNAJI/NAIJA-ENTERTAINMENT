/**
 * Category (archive) pages.
 * Each page: hero + filter chips + featured article + article stack + CTA band.
 */

const meta = (author, iso, date, minutes) => `
            <div class="mini-card__meta">
              <span>
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:-2px"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-6 8-6s8 2 8 6"/></svg>
                ${author}
              </span>
              <span class="dot">•</span><time datetime="${iso}">${date}</time>
              <span class="dot">•</span><span>${minutes} min read</span>
            </div>`;

const featureCard = (a) => `
          <article class="feature-card feature-card--spotlight reveal" data-tags="${a.tags}">
            <a href="${a.href}">
              <div class="media">
                <img src="${a.img}" alt="${a.alt}">
                <span class="media__tag">${a.tag}</span>
              </div>
              <div class="feature-card__body">
                <h3>${a.title}</h3>
                <p>${a.blurb}</p>${meta(a.author, a.iso, a.date, a.time)}
                <span class="feature-card__cta">Read full story <svg class="ico" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span>
              </div>
            </a>
          </article>`;

const miniCard = (a, hidden = false) => `
          <article class="mini-card reveal" data-tags="${a.tags}"${hidden ? ' data-more-item hidden' : ''}>
            <a class="media" href="${a.href}"><img src="${a.img}" alt="${a.alt}"></a>
            <div>
              <span class="tagline ${a.tagClass}">${a.tag}</span>
              <h4><a href="${a.href}">${a.title}</a></h4>
              <div class="mini-card__meta"><time datetime="${a.iso}">${a.date}</time><span class="dot">•</span><span>${a.time} min read</span></div>
            </div>
          </article>`;

const ctaForm = (title, text) => `
    <div class="cta__form">
      <input type="email" placeholder="Enter your email address" aria-label="Email address">
      <button class="btn btn--light" type="button" onclick="TNE_subscribe(this)">Subscribe</button>
    </div>`;

const page = ({ theme, img, alt, crumb, title, blurb, chips, heroActions, feature, stack, more, cta }) => `
<section class="page-hero ${theme}">
  <div class="hero-scene"><img src="${img}" alt="${alt}"></div>
  <div class="container page-hero__body">
    <nav class="crumbs"><a href="index.html">Home</a><span>›</span>${crumb}</nav>
    <h1>${title}</h1>
    <p>${blurb}</p>${heroActions ? `\n    <div class="page-hero__actions">${heroActions}</div>` : ''}
  </div>
</section>

<div class="container" data-filter-scope>
  <div class="filters" data-filter-group="this">
    <span class="filters__label">Filter:</span>
    ${chips.map((c, i) => `<button class="chip${i === 0 ? ' is-active' : ''}" data-filter="${c[0]}">${c[1]}</button>`).join('\n    ')}
  </div>

  <div class="cat-grid">
${featureCard(feature)}
    <div class="article-stack">
${stack.map((a) => miniCard(a)).join('\n')}
${more.map((a) => miniCard(a, true)).join('\n')}
    </div>
  </div>

  <div data-empty hidden style="text-align:center;color:var(--muted);font-size:13.5px;padding:30px 0">
    Nothing published in this filter yet — check back soon.
  </div>

  <div style="text-align:center;padding-bottom:8px" data-more-scope>
    <button class="btn btn--ghost btn--sm" type="button" data-more-btn>Load more articles</button>
  </div>
</div>

<section class="container" style="padding-bottom:12px">
${cta}
</section>
`;

/* ============================================================ */
const pages = [
  /* ---------------- FINANCE ---------------- */
  {
    file: 'category-finance.html',
    page: 'finance',
    active: 'finance',
    title: 'Finance — Practical financial tips, tools and resources',
    description: 'Learn how to budget, save, invest and grow your money in Nigeria with practical guides on personal finance, savings, banking and wealth building.',
    body: page({
      theme: 't-finance',
      img: 'assets/img/photos/coins.jpg',
      alt: 'Coin stacks with a growing plant',
      crumb: 'Finance',
      title: 'Finance',
      blurb: 'Practical financial tips, investment strategies, and tools to help you manage, grow and protect your money. Learn how to build wealth and financial freedom as a Nigerian entrepreneur.',
      heroActions: `<a class="btn btn--light" href="#latest">Browse Articles</a>
        <a class="btn btn--outline-light" href="category-crypto.html">Crypto &amp; Web3</a>`,
      chips: [['all', 'All'], ['investing', 'Investing'], ['personal', 'Personal Finance'], ['savings', 'Savings'], ['banking', 'Banking'], ['tips', 'Financial Tips']],
      feature: {
        tags: 'investing personal',
        href: 'article-10-profitable-business-ideas.html',
        img: 'assets/img/photos/desk.jpg',
        alt: 'Notebook, pen and savings jar on a study desk',
        tag: 'Featured',
        title: 'How to Build a Solid Investment Portfolio in Nigeria',
        blurb: 'Learn the investment options available to you, asset management tips and how to grow your wealth steadily — whether you are starting small or scaling up.',
        author: 'Ngozi Eze',
        iso: '2025-04-25',
        date: 'Apr 25, 2025',
        time: 6
      },
      stack: [
        { tags: 'savings personal tips', href: 'category-finance.html', img: 'assets/img/photos/laptop.jpg', alt: 'Budget chart on a laptop', tagClass: 'tag-green', tag: 'Savings', title: '7 Smart Ways to Save Money in Nigeria (Even on a Low Income)', iso: '2025-04-22', date: 'Apr 22, 2025', time: 7 },
        { tags: 'tips personal', href: 'category-finance.html', img: 'assets/img/photos/team.jpg', alt: 'Experts discussing money', tagClass: 'tag-orange', tag: 'Personal Finance', title: 'Understanding Inflation and How to Protect Your Money', iso: '2025-04-20', date: 'Apr 20, 2025', time: 5 },
        { tags: 'banking', href: 'category-finance.html', img: 'assets/img/photos/city.jpg', alt: 'Bank building in the city', tagClass: 'tag-blue', tag: 'Banking', title: 'The Best Nigerian Banks for Business Owners in 2025', iso: '2025-04-17', date: 'Apr 17, 2025', time: 6 },
        { tags: 'tips savings', href: 'category-finance.html', img: 'assets/img/photos/cafe.jpg', alt: 'Saving money at a cafe', tagClass: 'tag-green', tag: 'Financial Tips', title: 'Financial Freedom: 7 Habits of Successful Nigerians', iso: '2025-04-15', date: 'Apr 15, 2025', time: 8 }
      ],
      more: [
        { tags: 'investing', href: 'category-finance.html', img: 'assets/img/photos/crypto.jpg', alt: 'Digital assets', tagClass: 'tag-purple', tag: 'Investing', title: 'Stocks vs. Crypto: Where Should Nigerians Invest in 2025?', iso: '2025-04-12', date: 'Apr 12, 2025', time: 7 },
        { tags: 'banking tips', href: 'category-finance.html', img: 'assets/img/photos/founder.jpg', alt: 'Business owner reviewing finances', tagClass: 'tag-blue', tag: 'Banking', title: 'Getting a Business Loan in Nigeria: What Banks Look For', iso: '2025-04-10', date: 'Apr 10, 2025', time: 6 },
        { tags: 'savings personal', href: 'category-finance.html', img: 'assets/img/photos/ideas.jpg', alt: 'Written savings plan', tagClass: 'tag-green', tag: 'Savings', title: 'A Simple Budget Template That Works for Nigerian Households', iso: '2025-04-08', date: 'Apr 8, 2025', time: 5 }
      ],
      cta: `  <div class="cta reveal">
    <span class="cta__icon"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 17l5-6 4 4 5-8 4 5"/><path d="M3 21h18"/></svg></span>
    <div>
      <h3>Get smart with your money.</h3>
      <p>Subscribe for the latest finance tips and business guides.</p>
    </div>${ctaForm()}
  </div>`
    })
  },

  /* ---------------- BUSINESS ---------------- */
  {
    file: 'category-business.html',
    page: 'business',
    active: 'business',
    title: 'Business — News, strategies and growth ideas for Nigerian businesses',
    description: 'Business news, strategy, startups, small business and tools — practical resources for Nigerian entrepreneurs and business owners.',
    body: page({
      theme: 't-business',
      img: 'assets/img/photos/city.jpg',
      alt: 'City skyline at dusk',
      crumb: 'Business',
      title: 'Business',
      blurb: 'Business news, market trends, growth strategies and tools for Nigerian entrepreneurs and business owners.',
      heroActions: `<a class="btn btn--light" href="#latest">Browse Articles</a>
        <a class="btn btn--outline-light" href="category-entrepreneur.html">Startup Stories</a>`,
      chips: [['all', 'All'], ['news', 'Business News'], ['strategy', 'Strategy'], ['startups', 'Startups'], ['small', 'Small Business'], ['tools', 'Business Tools']],
      feature: {
        tags: 'strategy small',
        href: 'article-10-profitable-business-ideas.html',
        img: 'assets/img/photos/laptop.jpg',
        alt: 'Laptop on a desk with growth charts',
        tag: 'Featured',
        title: 'Nigerian SMEs: 5 Strategies to Survive and Thrive in 2025',
        blurb: 'Discover practical strategies to help small and medium businesses navigate challenges, secure funding, and achieve sustainable growth.',
        author: 'Ngozi Eze',
        iso: '2025-04-24',
        date: 'Apr 24, 2025',
        time: 6
      },
      stack: [
        { tags: 'strategy tools', href: 'category-business.html', img: 'assets/img/photos/ideas.jpg', alt: 'Notebook with a plan', tagClass: 'tag-blue', tag: 'Strategy', title: 'How to Write a Winning Business Plan', iso: '2025-04-21', date: 'Apr 21, 2025', time: 6 },
        { tags: 'news', href: 'category-business.html', img: 'assets/img/photos/phones.jpg', alt: 'Shopping on a phone', tagClass: 'tag-cyan', tag: 'Business News', title: 'The Rise of E-commerce in Nigeria', iso: '2025-04-18', date: 'Apr 18, 2025', time: 4 },
        { tags: 'small startups', href: 'category-business.html', img: 'assets/img/photos/team.jpg', alt: 'Founders meeting', tagClass: 'tag-orange', tag: 'Startups', title: '5 Nigerian Entrepreneurs Making Global Impact', iso: '2025-04-16', date: 'Apr 16, 2025', time: 7 },
        { tags: 'strategy', href: 'category-business.html', img: 'assets/img/photos/city.jpg', alt: 'Growing business district', tagClass: 'tag-blue', tag: 'Small Business', title: 'Business Opportunities in Nigeria’s Growing Sectors', iso: '2025-04-15', date: 'Apr 15, 2025', time: 8 }
      ],
      more: [
        { tags: 'tools', href: 'category-business.html', img: 'assets/img/photos/desk.jpg', alt: 'Bookkeeping desk', tagClass: 'tag-green', tag: 'Business Tools', title: '7 Free Tools Every Nigerian Small Business Needs', iso: '2025-04-13', date: 'Apr 13, 2025', time: 6 },
        { tags: 'news strategy', href: 'category-business.html', img: 'assets/img/photos/founder.jpg', alt: 'Entrepreneur reviewing results', tagClass: 'tag-blue', tag: 'Business News', title: 'What Nigeria’s New Tax Act Means for Your Business', iso: '2025-04-11', date: 'Apr 11, 2025', time: 5 },
        { tags: 'startups', href: 'category-business.html', img: 'assets/img/photos/startup.jpg', alt: 'Founder on a ridge', tagClass: 'tag-orange', tag: 'Startups', title: 'How to Register a Company in Nigeria: A Step-by-Step Guide', iso: '2025-04-09', date: 'Apr 9, 2025', time: 7 }
      ],
      cta: `  <div class="cta cta--blue reveal">
    <span class="cta__icon"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 20h18M7 20V10M12 20V4M17 20v-7"/></svg></span>
    <div>
      <h3>Grow Your Business</h3>
      <p>Get expert insights, tools and resources to scale your business.</p>
    </div>
    <div class="cta__actions">
      <a class="btn btn--light" href="category-business.html">Explore Resources <svg class="ico" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
    </div>
  </div>`
    })
  },

  /* ---------------- CRYPTO / WEB3 ---------------- */
  {
    file: 'category-crypto.html',
    page: 'crypto',
    active: 'crypto',
    title: 'Crypto / Web 3.0 — Blockchain news and opportunities',
    description: 'Blockchain, crypto news, Web3, DeFi and NFT insights for Nigerians — the next generation of on-chain business and investment.',
    body: page({
      theme: 't-crypto',
      img: 'assets/img/photos/crypto.jpg',
      alt: 'Crypto coins with a blockchain network',
      crumb: 'Crypto / Web 3.0',
      title: 'Crypto / Web 3.0',
      blurb: 'Blockchain, crypto news, Web3 innovations and opportunities for the next generation.',
      heroActions: `<a class="btn btn--light" href="#latest">Read the Latest</a>
        <a class="btn btn--outline-light" href="category-finance.html">Investing Basics</a>`,
      chips: [['all', 'All'], ['crypto', 'Crypto News'], ['web3', 'Web3'], ['blockchain', 'Blockchain'], ['defi', 'DeFi'], ['nfts', 'NFTs']],
      feature: {
        tags: 'crypto blockchain',
        href: 'article-10-profitable-business-ideas.html',
        img: 'assets/img/photos/crypto.jpg',
        alt: 'Bitcoin and altcoins',
        tag: 'Featured',
        title: 'Bitcoin Price Analysis: What to Expect in 2025',
        blurb: 'A deep dive into Bitcoin’s price trends, market sentiment and investment outlook — what experienced traders and analysts expect for the rest of the year.',
        author: 'Chinedu Okafor',
        iso: '2025-04-23',
        date: 'Apr 23, 2025',
        time: 7
      },
      stack: [
        { tags: 'crypto', href: 'category-crypto.html', img: 'assets/img/photos/crypto.jpg', alt: 'Altcoin list', tagClass: 'tag-purple', tag: 'Crypto News', title: 'Top 5 Altcoins to Watch in 2025', iso: '2025-04-20', date: 'Apr 20, 2025', time: 5 },
        { tags: 'web3', href: 'category-crypto.html', img: 'assets/img/photos/phones.jpg', alt: 'Web3 apps on a phone', tagClass: 'tag-cyan', tag: 'Web3', title: 'What is Web3 and Why It Matters', iso: '2025-04-18', date: 'Apr 18, 2025', time: 6 },
        { tags: 'defi', href: 'category-crypto.html', img: 'assets/img/photos/coins.jpg', alt: 'DeFi tokens', tagClass: 'tag-green', tag: 'DeFi', title: 'How to Get Started with DeFi', iso: '2025-04-16', date: 'Apr 16, 2025', time: 6 },
        { tags: 'crypto blockchain', href: 'category-crypto.html', img: 'assets/img/photos/desk.jpg', alt: 'Crypto wallet checklist', tagClass: 'tag-purple', tag: 'Wallets', title: 'Best Crypto Wallets for Nigerians', iso: '2025-04-14', date: 'Apr 14, 2025', time: 5 }
      ],
      more: [
        { tags: 'nfts', href: 'category-crypto.html', img: 'assets/img/photos/team.jpg', alt: 'Digital collectables', tagClass: 'tag-orange', tag: 'NFTs', title: 'NFTs in Nigeria: Creative Passions Meet Blockchain', iso: '2025-04-12', date: 'Apr 12, 2025', time: 6 },
        { tags: 'blockchain web3', href: 'category-crypto.html', img: 'assets/img/photos/city.jpg', alt: 'Distributed network over a city', tagClass: 'tag-blue', tag: 'Blockchain', title: 'Beyond Crypto: Real-World Use Cases of Blockchain in Nigeria', iso: '2025-04-10', date: 'Apr 10, 2025', time: 8 },
        { tags: 'defi crypto', href: 'category-crypto.html', img: 'assets/img/photos/founder.jpg', alt: 'Person using a crypto app', tagClass: 'tag-green', tag: 'DeFi', title: 'Yield Farming Explained for First-Time Users', iso: '2025-04-07', date: 'Apr 7, 2025', time: 7 }
      ],
      cta: `  <div class="cta cta--purple reveal">
    <span class="cta__icon"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg></span>
    <div>
      <h3>Stay Ahead in Web3</h3>
      <p>Get the latest crypto news, Web3 updates and opportunities.</p>
    </div>${ctaForm()}
  </div>`
    })
  },

  /* ---------------- ENTREPRENEUR CORNER ---------------- */
  {
    file: 'category-entrepreneur.html',
    page: 'entrepreneur',
    active: 'startup',
    title: 'Entrepreneur Corner — Inspiration, skills and funding',
    description: 'Inspiration, startup stories, skills, tools and resources for aspiring and existing Nigerian entrepreneurs — from idea to impact.',
    body: page({
      theme: 't-startup',
      img: 'assets/img/photos/startup.jpg',
      alt: 'Entrepreneur silhouette on a mountain ridge at sunrise',
      crumb: 'Entrepreneur Corner',
      title: 'Entrepreneur Corner',
      blurb: 'Inspiration, startup stories, skills, tools and resources for aspiring and existing entrepreneurs.',
      heroActions: `<a class="btn btn--light" href="#latest">Browse Articles</a>
        <a class="btn btn--outline-light" href="services.html">Free Resources</a>`,
      chips: [['all', 'All'], ['startups', 'Startups'], ['stories', 'Startup Stories'], ['skills', 'Skills & Tools'], ['funding', 'Funding'], ['motivation', 'Motivation']],
      feature: {
        tags: 'motivation stories',
        href: 'article-10-profitable-business-ideas.html',
        img: 'assets/img/photos/founder.jpg',
        alt: 'Founder smiling with a laptop',
        tag: 'Featured',
        title: 'From Idea to Impact: Lessons from Nigerian Founders',
        blurb: 'Real stories from entrepreneurs who turned small ideas into successful businesses — the setbacks, the strategies and the lessons they learned.',
        author: 'Ngozi Eze',
        iso: '2025-04-19',
        date: 'Apr 19, 2025',
        time: 8
      },
      stack: [
        { tags: 'startups skills', href: 'category-entrepreneur.html', img: 'assets/img/photos/ideas.jpg', alt: 'Testing a business idea', tagClass: 'tag-orange', tag: 'Startups', title: 'How to Validate Your Business Idea', iso: '2025-04-15', date: 'Apr 15, 2025', time: 6 },
        { tags: 'skills', href: 'category-entrepreneur.html', img: 'assets/img/photos/team.jpg', alt: 'Team working together', tagClass: 'tag-blue', tag: 'Skills & Tools', title: 'Essential Skills Every Entrepreneur Needs', iso: '2025-04-12', date: 'Apr 12, 2025', time: 7 },
        { tags: 'funding', href: 'category-entrepreneur.html', img: 'assets/img/photos/city.jpg', alt: 'Investors meeting', tagClass: 'tag-cyan', tag: 'Funding', title: 'Accessing Funding as a Nigerian Startup', iso: '2025-04-10', date: 'Apr 10, 2025', time: 6 },
        { tags: 'motivation', href: 'category-entrepreneur.html', img: 'assets/img/photos/startup.jpg', alt: 'Climbing the next mountain', tagClass: 'tag-orange', tag: 'Motivation', title: 'Overcoming Challenges as a Young Entrepreneur', iso: '2025-04-08', date: 'Apr 8, 2025', time: 6 }
      ],
      more: [
        { tags: 'stories', href: 'category-entrepreneur.html', img: 'assets/img/photos/laptop.jpg', alt: 'Founder at work', tagClass: 'tag-green', tag: 'Startup Stories', title: 'How a Lagos Side Hustle Became a ₦50M Yearly Business', iso: '2025-04-06', date: 'Apr 6, 2025', time: 7 },
        { tags: 'funding startups', href: 'category-entrepreneur.html', img: 'assets/img/photos/cafe.jpg', alt: 'Pitch meeting over coffee', tagClass: 'tag-blue', tag: 'Funding', title: 'Grants and Programs Nigerian Founders Can Apply For', iso: '2025-04-04', date: 'Apr 4, 2025', time: 8 },
        { tags: 'skills tools', href: 'category-entrepreneur.html', img: 'assets/img/photos/desk.jpg', alt: 'Planning a launch', tagClass: 'tag-purple', tag: 'Skills & Tools', title: 'Project Management Basics for Busy Founders', iso: '2025-04-02', date: 'Apr 2, 2025', time: 6 }
      ],
      cta: `  <div class="cta cta--orange reveal">
    <span class="cta__icon"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M13 2 4 14h6l-1 8 9-12h-6z"/></svg></span>
    <div>
      <h3>Turn Your Idea Into a Business</h3>
      <p>Get resources, mentorship and tools to help you grow.</p>
    </div>
    <div class="cta__actions">
      <a class="btn btn--light" href="contact.html">Explore More <svg class="ico" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
    </div>
  </div>`
    })
  },

  /* ---------------- AFFILIATES ---------------- */
  {
    file: 'category-affiliates.html',
    page: 'affiliates',
    active: 'affiliate',
    title: 'Affiliates — Make money online with affiliate marketing',
    description: 'Affiliate marketing, online income, programs and proven strategies — learn how to make money online in Nigeria as an affiliate marketer.',
    body: page({
      theme: 't-affiliate',
      img: 'assets/img/photos/phones.jpg',
      alt: 'Hand holding a phone showing an affiliate dashboard',
      crumb: 'Affiliates',
      title: 'Affiliates',
      blurb: 'Make money online, affiliate programs, and digital opportunities — join our growing community of smart earners.',
      heroActions: `<a class="btn btn--light" href="#latest">Browse Articles</a>
        <a class="btn btn--outline-light" href="contact.html">Join the Community</a>`,
      chips: [['all', 'All'], ['marketing', 'Affiliate Marketing'], ['online', 'Online Income'], ['programs', 'Programs'], ['guides', 'Tips & Guides']],
      feature: {
        tags: 'marketing guides',
        href: 'article-10-profitable-business-ideas.html',
        img: 'assets/img/photos/phones.jpg',
        alt: 'Affiliate dashboard on a smartphone',
        tag: 'Featured',
        title: 'Step-by-Step Guide to Making Money with Affiliate Marketing in Nigeria',
        blurb: 'Step-by-step tutorial on getting started and earning online — practical strategies for building traffic and converting clicks into income.',
        author: 'Ngozi Eze',
        iso: '2025-04-18',
        date: 'Apr 18, 2025',
        time: 10
      },
      stack: [
        { tags: 'programs', href: 'category-affiliates.html', img: 'assets/img/photos/crypto.jpg', alt: 'Program list', tagClass: 'tag-purple', tag: 'Programs', title: 'Top 10 Best Affiliate Programs for Nigerians', iso: '2025-04-16', date: 'Apr 16, 2025', time: 7 },
        { tags: 'marketing guides', href: 'category-affiliates.html', img: 'assets/img/photos/laptop.jpg', alt: 'Blog being written', tagClass: 'tag-green', tag: 'Tips & Guides', title: 'How to Create a High-Converting Blog', iso: '2025-04-14', date: 'Apr 14, 2025', time: 8 },
        { tags: 'online', href: 'category-affiliates.html', img: 'assets/img/photos/coins.jpg', alt: 'Passive income coins', tagClass: 'tag-blue', tag: 'Online Income', title: 'Passive Income Ideas for 2025', iso: '2025-04-12', date: 'Apr 12, 2025', time: 6 },
        { tags: 'marketing', href: 'category-affiliates.html', img: 'assets/img/photos/team.jpg', alt: 'Marketing meeting', tagClass: 'tag-orange', tag: 'Affiliate Marketing', title: 'Affiliate Marketing Mistakes to Avoid', iso: '2025-04-10', date: 'Apr 10, 2025', time: 6 }
      ],
      more: [
        { tags: 'online', href: 'category-affiliates.html', img: 'assets/img/photos/ideas.jpg', alt: 'Digital product ideas', tagClass: 'tag-cyan', tag: 'Online Income', title: 'Selling Digital Products in Nigeria: A Beginner’s Roadmap', iso: '2025-04-08', date: 'Apr 8, 2025', time: 7 },
        { tags: 'guides', href: 'category-affiliates.html', img: 'assets/img/photos/founder.jpg', alt: 'Creator with a camera', tagClass: 'tag-blue', tag: 'Tips & Guides', title: 'Using Short-Form Video to Drive Affiliate Sales', iso: '2025-04-06', date: 'Apr 6, 2025', time: 6 },
        { tags: 'programs online', href: 'category-affiliates.html', img: 'assets/img/photos/city.jpg', alt: 'Global affiliate network', tagClass: 'tag-green', tag: 'Programs', title: 'How Affiliate Payments Work: Payout Methods Nigerians Can Use', iso: '2025-04-03', date: 'Apr 3, 2025', time: 5 }
      ],
      cta: `  <div class="cta cta--cyan reveal">
    <span class="cta__icon"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M17 3h4v4"/><path d="M21 3 11 13"/><path d="M8 21H5a2 2 0 0 1-2-2v-3M15 21h4a2 2 0 0 0 2-2v-3"/></svg></span>
    <div>
      <h3>Start Earning Online</h3>
      <p>Join 50+ affiliate programs and earn with proven strategies.</p>
    </div>
    <div class="cta__actions">
      <a class="btn btn--light" href="contact.html">Get Started <svg class="ico" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
    </div>
  </div>`
    })
  }
];

export default pages;
