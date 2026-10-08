/**
 * Standalone pages: article, services, about, contact, privacy policy, 404.
 */

const socials = `
        <div class="socials">
          <a class="s-x" href="#" aria-label="X">X</a>
          <a class="s-f" href="#" aria-label="Facebook">f</a>
          <a class="s-wa" href="#" aria-label="WhatsApp">W</a>
          <a class="s-in" href="#" aria-label="LinkedIn">in</a>
          <a class="s-ig" href="#" aria-label="Instagram">ig</a>
          <a class="s-yt" href="#" aria-label="YouTube">▶</a>
        </div>`;

const newsletterWidget = `
    <section class="widget reveal">
      <div class="widget__head">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>
        Join Our Newsletter
      </div>
      <div class="widget__body">
        <form class="newsletter-form" data-newsletter novalidate>
          <p style="font-size:13px;color:var(--muted);margin:0">Get fresh business, finance and crypto insights every week.</p>
          <input type="email" name="email" placeholder="Enter your email address" aria-label="Email address" required>
          <button class="btn btn--primary btn--block" type="submit">Subscribe</button>
          <p class="newsletter-note" data-form-status role="status"></p>
        </form>
      </div>
    </section>`;

const followWidget = `
    <section class="widget reveal">
      <div class="widget__head">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 3v18M3 12h18"/></svg>
        Follow Us
      </div>
      <div class="widget__body">${socials}</div>
    </section>`;

const sidebar = (inner) => `
  <aside class="sidebar">${inner}
  </aside>`;

/* ============================================================ */
const pages = [
  /* ---------------- ARTICLE ---------------- */
  {
    file: 'article-10-profitable-business-ideas.html',
    page: 'article',
    title: '10 Profitable Business Ideas Nigerian Founders Can Start in 2025',
    description: 'Starting a business in Nigeria has never been more accessible. Here are 10 profitable business ideas Nigerian founders can start in 2025.',
    body: `
<section class="container section" style="padding-top:18px">
  <nav class="crumbs"><a href="index.html">Home</a><span>›</span><a href="category-business.html">Business</a><span>›</span>Business Ideas</nav>

  <div class="cat-grid">
    <article class="feature-card reveal" style="grid-column:1/-1">
      <div class="media article-hero" style="aspect-ratio:16/7">
        <img src="assets/img/scene-ideas.svg" alt="Open notebook filled with business ideas">
        <span class="media__tag">Business Ideas</span>
      </div>
      <div class="feature-card__body">
        <h1>10 Profitable Business Ideas Nigerian Founders Can Start in 2025</h1>
        <p style="font-size:16px;color:var(--ink-2);max-width:70ch">Starting a business in Nigeria has never been more accessible. With rising internet penetration, widespread mobile money adoption, and a vibrant startup ecosystem, entrepreneurs are turning ideas into income faster than ever.</p>
        <div class="mini-card__meta" style="margin-top:6px">
          <span><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:-2px"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-6 8-6s8 2 8 6"/></svg> Ngozi Eze</span>
          <span class="dot">•</span><time datetime="2025-04-29">Apr 29, 2025</time>
          <span class="dot">•</span><span>6 min read</span>
          <span class="dot">•</span><span class="badge-live">Updated for 2025</span>
        </div>
      </div>
    </article>
  </div>
</section>

<div class="container article-layout">
  <div>
    <section class="panel reveal">
      <div class="panel__head">Article</div>
      <div class="article-body">
        <h2 id="intro">Introduction</h2>
        <p>Nigeria’s business landscape has changed dramatically. A generation ago, starting a company meant significant capital, formal office space and years of waiting. Today, a smartphone, a clear idea and consistent effort are enough to begin earning — many of our most successful readers started exactly that way.</p>

        <div class="callout">
          <strong>Short answer</strong>
          <p>The best business for you is the one that solves a real problem for real people, at a price they can pay, in a way you can repeat. Everything else is detail.</p>
        </div>

        <h2 id="why">Why These Ideas Matter</h2>
        <p>Nigeria’s economy is projected to grow significantly over the next decade, creating millions of new jobs and business opportunities. Ideas that solve everyday problems — transportation, food, education, healthcare, or financial access — tend to gain traction quickest because the need is already proven.</p>
        <p>The advantage goes to founders who start small and learn fast. You do not need a perfect product; you need a usable one, real feedback, and the willingness to adjust.</p>

        <h2 id="what-you-need">What You Need to Get Started</h2>
        <ul class="checklist">
          <li>A clear business idea — written down in one sentence</li>
          <li>A simple budget, even if it is only tens of thousands of naira</li>
          <li>A smartphone or laptop and reliable internet access</li>
          <li>A registered business name with the CAC</li>
          <li>A way to track sales, costs and customer feedback</li>
        </ul>

        <h2 id="quick-wins">Quick Wins You Can Start Today</h2>
        <p>Some of these can produce income within weeks rather than months:</p>
        <ul>
          <li><strong>Freelance services</strong> — writing, design, video editing, translation, virtual assistance</li>
          <li><strong>Reselling online</strong> — curated products, phone accessories, beauty and fashion items</li>
          <li><strong>Mobile food service</strong> — local dishes with dependable quality and packaging</li>
          <li><strong>Tutoring or coaching</strong> — school subjects, skills training, exam preparation</li>
          <li><strong>Social media management</strong> — content, community and ads for small businesses</li>
        </ul>

        <h2 id="choose">How to Choose the Right Idea for You</h2>
        <ul class="checklist">
          <li>Start with a problem you understand — lived experience beats guesswork</li>
          <li>Test before investing heavily — run a small pilot, measure, then scale</li>
          <li>Start small, scale smart — grow revenue before growing costs</li>
          <li>Track your numbers from day one — know your margin and your break-even point</li>
        </ul>

        <h2 id="conclusion">Conclusion</h2>
        <p>The best business is the one you will actually start. Choose an idea that fits your skills, budget and schedule, then give it ninety days of honest effort. Consistency compounds faster than capital in Nigeria today — and the founders who win are usually the ones who kept going after the first difficult month.</p>

        <div class="share-row">
          <span>Share this article</span>${socials}
          <button class="btn btn--ghost btn--sm" type="button" data-copy-link style="margin-left:auto">🔗 Copy link</button>
        </div>
      </div>
    </section>

    <section class="panel reveal" style="margin-top:18px">
      <div class="panel__head">Keep reading</div>
      <div class="panel__body">
        <div class="card-grid-2">
          <article class="mini-card reveal">
            <a class="media" href="category-finance.html"><img src="assets/img/scene-coins.svg" alt="Coin stacks"></a>
            <div><span class="tagline tag-green">Investing</span><h4><a href="category-finance.html">How to Build a Solid Investment Portfolio in Nigeria</a></h4><div class="mini-card__meta"><time datetime="2025-04-25">Apr 25, 2025</time><span class="dot">•</span><span>6 min read</span></div></div>
          </article>
          <article class="mini-card reveal">
            <a class="media" href="category-business.html"><img src="assets/img/scene-laptop.svg" alt="Laptop with charts"></a>
            <div><span class="tagline tag-blue">Strategy</span><h4><a href="category-business.html">Nigerian SMEs: 5 Strategies to Survive and Thrive in 2025</a></h4><div class="mini-card__meta"><time datetime="2025-04-24">Apr 24, 2025</time><span class="dot">•</span><span>6 min read</span></div></div>
          </article>
        </div>
      </div>
    </section>
  </div>

${sidebar(`    <section class="widget reveal">
      <div class="widget__head">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 6h16M4 12h16M4 18h10"/></svg>
        Table of Contents
      </div>
      <div class="widget__body">
        <ol class="toc" data-spy>
          <li><a href="#intro">Introduction</a></li>
          <li><a href="#why">Why These Ideas Matter</a></li>
          <li><a href="#what-you-need">What You Need</a></li>
          <li><a href="#quick-wins">Quick Wins</a></li>
          <li><a href="#choose">Choosing the Right Idea</a></li>
          <li><a href="#conclusion">Conclusion</a></li>
        </ol>
      </div>
    </section>
    <section class="widget reveal">
      <div class="widget__head">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M17 3h4v4"/><path d="M21 3 11 13"/><path d="M8 21H5a2 2 0 0 1-2-2v-3"/></svg>
        Share This Article
      </div>
      <div class="widget__body">${socials}</div>
    </section>
${newsletterWidget}
${followWidget}
    <section class="widget reveal">
      <div class="widget__head">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 4h12v16l-6-4-6 4z"/></svg>
        Popular Posts
      </div>
      <div class="widget__body">
        <ol class="popular">
          <li><a href="article-10-profitable-business-ideas.html">10 Profitable Business Ideas Nigerian Founders Can Start in 2025<small>Apr 30, 2025 · 6 min read</small></a></li>
          <li><a href="category-finance.html">How to Build a Solid Investment Portfolio in Nigeria<small>Apr 25, 2025 · 6 min read</small></a></li>
          <li><a href="category-crypto.html">Bitcoin Price Analysis: What to Expect in 2025<small>Apr 23, 2025 · 7 min read</small></a></li>
          <li><a href="category-entrepreneur.html">From Idea to Impact: Lessons from Nigerian Founders<small>Apr 19, 2025 · 8 min read</small></a></li>
        </ol>
      </div>
    </section>`)}
</div>`
  },

  /* ---------------- SERVICES ---------------- */
  {
    file: 'services.html',
    page: 'services',
    title: 'Our Services — Resources, guidance and community for entrepreneurs',
    description: 'We provide reliable resources and tools to help you grow: business resources, affiliate guidance, consultation, digital products and community access.',
    body: `
<section class="page-hero t-services">
  <div class="hero-scene"><img src="assets/img/scene-cafe.svg" alt="Coffee and laptop workspace"></div>
  <div class="container page-hero__body">
    <nav class="crumbs"><a href="index.html">Home</a><span>›</span>Services</nav>
    <h1>Our Services</h1>
    <p>We provide reliable resources and tools to help you grow.</p>
  </div>
</section>

<div class="container">
  <div class="service-grid">
    <article class="service-card reveal">
      <span class="service-card__icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 5h13a2 2 0 0 1 2 2v12H6a2 2 0 0 1-2-2z"/><path d="M19 19H8a2 2 0 0 1-2-2"/><path d="M8 9h7M8 13h5"/></svg></span>
      <h3>Blog &amp; News</h3>
      <p>Daily updates and insights on business, finance and technology — straight to your inbox and on every major platform.</p>
      <a class="link-more" href="category-business.html">Learn More</a>
    </article>

    <article class="service-card reveal">
      <span class="service-card__icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 12h18"/></svg></span>
      <h3>Business Resources</h3>
      <p>Templates, guides and tools to help you grow your business — from idea to scale.</p>
      <a class="link-more" href="category-business.html">Learn More</a>
    </article>

    <article class="service-card reveal">
      <span class="service-card__icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M17 3h4v4"/><path d="M21 3 11 13"/><path d="M8 21H5a2 2 0 0 1-2-2v-3"/></svg></span>
      <h3>Affiliate Guidance</h3>
      <p>Step-by-step guides to start and grow your affiliate marketing journey.</p>
      <a class="link-more" href="category-affiliates.html">Learn More</a>
    </article>

    <article class="service-card reveal">
      <span class="service-card__icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 15a2 2 0 0 1-2 2H8l-4 4V5a2 2 0 0 1 2-2h13a2 2 0 0 1 2 2z"/></svg></span>
      <h3>Consultation &amp; Tips</h3>
      <p>Expert advice, practical tips and mentorship tailored to your goals.</p>
      <a class="link-more" href="contact.html">Learn More</a>
    </article>

    <article class="service-card reveal">
      <span class="service-card__icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="4" width="18" height="14" rx="2"/><path d="M8 21h8M12 18v3"/></svg></span>
      <h3>Digital Products</h3>
      <p>E-books, courses and resources that make entrepreneurship easier.</p>
      <a class="link-more" href="category-business.html">Learn More</a>
    </article>

    <article class="service-card reveal">
      <span class="service-card__icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="9" cy="8" r="3"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17" cy="9" r="2.5"/><path d="M16 14.5c2.8.3 5 2.5 5 5.5"/></svg></span>
      <h3>Community Access</h3>
      <p>Join our growing community of entrepreneurs learning and growing together.</p>
      <a class="link-more" href="contact.html">Learn More</a>
    </article>
  </div>
</div>

<section class="container" style="padding-bottom:12px">
  <div class="cta reveal">
    <span class="cta__icon"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg></span>
    <div>
      <h3>Need Personalized Support?</h3>
      <p>Get expert advice and consultation tailored to your goals.</p>
    </div>
    <div class="cta__actions">
      <a class="btn btn--light" href="contact.html">Download List →</a>
    </div>
  </div>
</section>`
  },

  /* ---------------- ABOUT ---------------- */
  {
    file: 'about.html',
    page: 'about',
    title: 'About Us — The Nigerian Entrepreneur',
    description: 'The Nigerian Entrepreneur is a leading blog platform dedicated to promoting entrepreneurship and financial literacy in Nigeria, inspiring a new generation of wealth creators.',
    body: `
<section class="page-hero t-about">
  <div class="hero-scene"><img src="assets/img/scene-founder.svg" alt="Founder of The Nigerian Entrepreneur at work"></div>
  <div class="container page-hero__body">
    <nav class="crumbs"><a href="index.html">Home</a><span>›</span>About Us</nav>
    <h1>About Us</h1>
    <p>Our mission is to empower Nigerian entrepreneurs with the knowledge, tools and opportunities to build wealth and contribute to a prosperous and equitable society.</p>
  </div>
</section>

<div class="container">
  <div class="split">
    <div class="panel reveal" style="padding:26px">
      <div class="logo-big">
        <span class="logo__mark">NE</span>
        <span class="logo__text">The Nigerian<span>Entrepreneur</span></span>
      </div>
    </div>

    <div class="reveal">
      <h2 class="section__title">Who We Are</h2>
      <p><strong>The Nigerian Entrepreneur</strong> is a leading blog platform dedicated to promoting entrepreneurship and financial literacy in finance, business, technology, and more.</p>
      <p>We are passionate about helping Nigerians turn ideas into wealth, build a career as entrepreneurs and achieve financial freedom.</p>
      <p>We provide value by sharing useful business insights and financial tips, promoting entrepreneurship and more.</p>

      <div class="badge-row">
        <span class="badge"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M13 2 4 14h6l-1 8 9-12h-6z"/></svg> Inspire <small style="font-weight:500;color:var(--muted)">— share inspiring stories</small></span>
        <span class="badge"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 3 2 8l10 5 10-5z"/><path d="M6 11v5c0 1.7 2.7 3 6 3s6-1.3 6-3v-5"/></svg> Educate <small style="font-weight:500;color:var(--muted)">— provide knowledge and tools</small></span>
        <span class="badge"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 3a9 9 0 1 0 9 9"/><path d="M12 3v9l6 3"/></svg> Empower <small style="font-weight:500;color:var(--muted)">— provide opportunities</small></span>
      </div>

      <div class="stat-row">
        <div class="stat"><b>250k+</b><span>Monthly readers</span></div>
        <div class="stat"><b>1,200+</b><span>Articles published</span></div>
        <div class="stat"><b>50+</b><span>Partner programs</span></div>
      </div>
    </div>
  </div>

  <div class="vision reveal">
    <div class="vision__grid">
      <div>
        <h2 class="section__title" style="margin-top:0">Our Vision</h2>
        <p style="margin:0 0 8px">A Nigeria where every entrepreneur has access to the knowledge, tools and opportunity to succeed.</p>
        <p style="margin:0">We measure our progress by the businesses that start, the jobs created and the households that become financially secure because of something we published.</p>
        <div class="page-hero__actions">
          <a class="btn btn--primary" href="contact.html">Work With Us</a>
          <a class="btn btn--ghost" href="services.html">See Our Services</a>
        </div>
      </div>
      <div class="vision__art">
        <img src="assets/img/scene-city.svg" alt="City skyline representing economic opportunity">
      </div>
    </div>
  </div>

  <div style="padding:26px 0 8px">
    <div class="headline-row">
      <h2 class="section__title" style="margin:0">What we cover</h2>
    </div>
    <div class="cat-cards">
      <a class="cat-card cc-finance reveal" href="category-finance.html"><span class="cat-card__icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 17l5-6 4 4 5-8 4 5"/><path d="M3 21h18"/></svg></span><h3>Finance</h3><p>Investing, saving and protecting your money.</p><span class="cat-card__arrow">Explore →</span></a>
      <a class="cat-card cc-business reveal" href="category-business.html"><span class="cat-card__icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg></span><h3>Business</h3><p>News, strategy and growth for small businesses.</p><span class="cat-card__arrow">Explore →</span></a>
      <a class="cat-card cc-crypto reveal" href="category-crypto.html"><span class="cat-card__icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/></svg></span><h3>Crypto / Web 3.0</h3><p>Blockchain news and the next generation of finance.</p><span class="cat-card__arrow">Explore →</span></a>
      <a class="cat-card cc-startup reveal" href="category-entrepreneur.html"><span class="cat-card__icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg></span><h3>Entrepreneur Corner</h3><p>Stories, skills and funding for founders.</p><span class="cat-card__arrow">Explore →</span></a>
      <a class="cat-card cc-affiliate reveal" href="category-affiliates.html"><span class="cat-card__icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M17 3h4v4"/><path d="M21 3 11 13"/></svg></span><h3>Affiliates</h3><p>Make money online with proven strategies.</p><span class="cat-card__arrow">Explore →</span></a>
    </div>
  </div>
</div>`
  },

  /* ---------------- CONTACT ---------------- */
  {
    file: 'contact.html',
    page: 'contact',
    title: 'Contact Us — The Nigerian Entrepreneur',
    description: 'Have a question, proposal or need support? Send us a message and our team will reply within one business day.',
    body: `
<section class="page-hero t-business">
  <div class="hero-scene"><img src="assets/img/scene-city.svg" alt="City skyline at night"></div>
  <div class="container page-hero__body">
    <nav class="crumbs"><a href="index.html">Home</a><span>›</span>Contact</nav>
    <h1>Contact Us</h1>
    <p>Have a question, proposal or need support? We’d love to hear from you.</p>
  </div>
</section>

<div class="container two-col">
  <section class="panel reveal">
    <div class="panel__head">Send Us a Message</div>
    <div class="panel__body">
      <form data-contact novalidate>
        <div class="form-grid">
          <div class="field">
            <label for="fullName">Full Name *</label>
            <input type="text" id="fullName" name="fullName" placeholder="Your full name" autocomplete="name" required>
          </div>
          <div class="field">
            <label for="email">Email Address *</label>
            <input type="email" id="email" name="email" placeholder="you@example.com" autocomplete="email" required>
          </div>
          <div class="field field--full">
            <label for="subject">Subject *</label>
            <select id="subject" name="subject" required>
              <option value="">Choose a topic</option>
              <option>General enquiry</option>
              <option>Advertising &amp; partnerships</option>
              <option>Affiliate programme</option>
              <option>Editorial / guest post</option>
              <option>Technical support</option>
            </select>
          </div>
          <div class="field field--full">
            <label for="message">Your Message *</label>
            <textarea id="message" name="message" placeholder="Tell us how we can help…" required></textarea>
          </div>
          <div class="field field--full">
            <label class="check"><input type="checkbox" name="agree" required> <span>I agree to the <a href="privacy-policy.html" style="color:var(--green-700);font-weight:700">privacy policy</a> and consent to being contacted about my enquiry.</span></label>
          </div>
          <div class="field field--full">
            <p class="form-status" data-form-status role="status"></p>
          </div>
          <div class="field field--full">
            <button class="btn btn--primary" type="submit">Send Message</button>
          </div>
        </div>
      </form>
    </div>
  </section>

${sidebar(`    <section class="widget reveal">
      <div class="widget__head">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 10c0 7-9 12-9 12S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
        Our Contact Details
      </div>
      <div class="widget__body">
        <ul class="info-list">
          <li>
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 10c0 7-9 12-9 12S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            <span><strong>Location</strong>Lagos, Nigeria<br>Remote-first team</span>
          </li>
          <li>
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>
            <span><strong>Email</strong><a href="mailto:info@thenigerianentrepreneur.com" style="color:var(--green-700);font-weight:600">info@thenigerianentrepreneur.com</a><br>Replies within 1 business day</span>
          </li>
          <li>
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8"/></svg>
            <span><strong>Phone</strong><a href="tel:+2348000000000" style="color:var(--green-700);font-weight:600">+234 800 000 0000</a><br>Mon–Fri, 9am – 5pm WAT</span>
          </li>
          <li>
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>
            <span><strong>Response time</strong>Same working day for most messages</span>
          </li>
        </ul>
        <div style="border-top:1px solid var(--line);padding-top:14px">
          <strong style="font-size:12.5px;display:block;margin-bottom:8px">Follow Us</strong>${socials}
        </div>
      </div>
    </section>

    <section class="widget reveal">
      <div class="widget__head">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M13 2 4 14h6l-1 8 9-12h-6z"/></svg>
        Let’s Build Together
      </div>
      <div class="widget__body">
        <div class="promo">
          <h4>Partner With Us</h4>
          <p>Full-scale brand collaboration, growth, paid promotions and more.</p>
          <a class="btn btn--light btn--sm" href="mailto:partnerships@thenigerianentrepreneur.com">Talk to Us →</a>
        </div>
      </div>
    </section>

    <section class="widget reveal">
      <div class="widget__head">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 3v18M3 12h18"/></svg>
        Quick Links
      </div>
      <div class="widget__body">
        <ol class="toc">
          <li><a href="services.html">Our Services</a></li>
          <li><a href="category-business.html">Business Resources</a></li>
          <li><a href="category-affiliates.html">Affiliate Guidance</a></li>
          <li><a href="privacy-policy.html">Privacy Policy</a></li>
        </ol>
      </div>
    </section>`)}
</div>`
  },

  /* ---------------- PRIVACY POLICY ---------------- */
  {
    file: 'privacy-policy.html',
    page: 'privacy',
    title: 'Privacy Policy — The Nigerian Entrepreneur',
    description: 'Your privacy matters. Read how The Nigerian Entrepreneur collects, uses, stores and protects your personal information.',
    body: `
<section class="page-hero t-about">
  <div class="hero-scene"><img src="assets/img/scene-mesh.svg" alt="Secure abstract backdrop"></div>
  <div class="container page-hero__body">
    <nav class="crumbs"><a href="index.html">Home</a><span>›</span>Privacy Policy</nav>
    <h1>Privacy Policy</h1>
    <p>Your privacy matters. Here’s how we protect your information.</p>
  </div>
</section>

<div class="container legal">
  <section class="widget legal__toc reveal">
    <div class="widget__head">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 3 4 6v6c0 5 3.4 8.4 8 9 4.6-.6 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/></svg>
      On this page
    </div>
    <div class="widget__body">
      <ol data-spy>
        <li><a href="#introduction">Introduction<small>How we handle your data</small></a></li>
        <li><a href="#information-we-collect">Information We Collect<small>What we gather and why</small></a></li>
        <li><a href="#how-we-use-your-information">How We Use Your Information<small>Purpose of your data</small></a></li>
        <li><a href="#contact-us">Contact Us<small>Get in touch</small></a></li>
        <li><a href="#cookies">Cookies<small>How we use cookies</small></a></li>
        <li><a href="#our-commitment">Our Commitment<small>Keeping your data safe</small></a></li>
      </ol>
    </div>
  </section>

  <article class="panel reveal">
    <div class="article-body">
      <div class="privacy-note">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" style="flex:none;margin-top:1px"><circle cx="12" cy="12" r="9"/><path d="M12 8h.01M11 12h1v4h1"/></svg>
        <div><strong>Last updated: January 2025</strong>By using this website you agree to the practices described on this page. Questions? <a href="#contact-us" style="font-weight:700">Contact us</a>.</div>
      </div>

      <h2 id="introduction">1. Introduction</h2>
      <p>The Nigerian Entrepreneur (“we”, “us”, or “our”) operates <a href="index.html" style="color:var(--green-700);font-weight:700">thenigerianentrepreneur.com</a>. This privacy policy explains what information we collect through your use of our website, how we use that information to deliver the resources and community you signed up for, and the steps we take to keep it safe.</p>

      <h2 id="information-we-collect">2. Information We Collect</h2>
      <p>We collect only the information that helps us serve you better:</p>
      <ul>
        <li><strong>Basic contact details</strong> — such as your name and email address, which you provide when you subscribe to our newsletter, download a resource or contact us.</li>
        <li><strong>Usage data</strong> — pages you visit, articles you read, the device and browser you use, and the approximate region you connect from. This helps us understand which topics matter most.</li>
        <li><strong>Voluntary submissions</strong> — including guest post pitches, partnership enquiries and feedback you send through our contact form.</li>
      </ul>
      <p>We do not knowingly collect information from children under 16, and we never sell personal information to anyone.</p>

      <h2 id="how-we-use-your-information">3. How We Use Your Information</h2>
      <p>We use your information to:</p>
      <ul>
        <li>Provide and update our services — newsletters, articles, guides and community access.</li>
        <li>Improve our content by understanding which resources are most valuable.</li>
        <li>Communicate with you — replies to enquiries, service updates and the occasional article you asked to receive.</li>
        <li>Detect and prevent abuse, spam or fraud against our platform.</li>
      </ul>

      <h2 id="contact-us">4. Contact Us</h2>
      <p>If you have any questions, suggestions or concerns about our privacy practices, please reach out and we will respond promptly.</p>
      <ul>
        <li><strong>Email:</strong> <a href="mailto:info@thenigerianentrepreneur.com" style="color:var(--green-700);font-weight:700">info@thenigerianentrepreneur.com</a></li>
        <li><strong>Location:</strong> Lagos, Nigeria</li>
        <li><strong>Response time:</strong> within one business day</li>
      </ul>

      <h2 id="cookies">5. Cookies</h2>
      <p>We use cookies and similar technologies to operate the site effectively:</p>
      <ul>
        <li><strong>Essential cookies</strong> — required for core site functionality and cannot be disabled.</li>
        <li><strong>Analytics cookies</strong> — help us understand how visitors use the site so we can improve it.</li>
        <li><strong>Preference cookies</strong> — remember settings such as your newsletter status.</li>
      </ul>
      <p>You can accept, reject or delete cookies through your browser settings at any time. Disabling certain cookies may affect how parts of the site behave.</p>

      <h2 id="our-commitment">6. Our Commitment</h2>
      <p>We are committed to protecting your privacy and will never share your data without your consent. We continuously review our practices to ensure we meet global data protection standards and the requirements of the Nigerian Data Protection Act.</p>

      <div class="share-row">
        <span>Was this page helpful?</span>
        <button class="btn btn--ghost btn--sm" type="button" onclick="document.dispatchEvent(new CustomEvent('tne:toast',{detail:'Thanks for the feedback!'}))">Yes, thanks</button>
      </div>
    </div>
  </article>
</div>`
  },

  /* ---------------- 404 ---------------- */
  {
    file: '404.html',
    page: '404',
    title: 'Page Not Found — The Nigerian Entrepreneur',
    description: 'The page you are looking for could not be found. Go back home or search the site.',
    body: `
<div class="container nf">
  <div class="nf__bubbles"><i></i><i></i><i></i><i></i><i></i></div>
  <div class="nf__code" aria-label="404">
    <b>4</b>
    <span class="zero" aria-hidden="true">
      <svg viewBox="0 0 100 100">
        <defs>
          <linearGradient id="z404" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stop-color="#0a4a2e"/><stop offset="1" stop-color="#12a35d"/>
          </linearGradient>
        </defs>
        <circle cx="50" cy="50" r="42" fill="none" stroke="url(#z404)" stroke-width="9"/>
        <circle cx="50" cy="50" r="42" fill="none" stroke="#dff5e9" stroke-width="9" stroke-dasharray="40 224" stroke-linecap="round"/>
        <circle cx="50" cy="50" r="24" fill="none" stroke="#e6f6ed" stroke-width="7" stroke-dasharray="24 127" stroke-linecap="round"/>
        <circle cx="50" cy="26" r="5" fill="#e6f6ed"/>
      </svg>
    </span>
    <b>4</b>
  </div>
  <h2>Page Not Found</h2>
  <p>The page you’re looking for might have been moved, renamed, or it may no longer exist. Try searching, or head back to familiar ground.</p>
  <div class="nf__actions">
    <a class="btn btn--primary" href="index.html">Go Back Home</a>
    <a class="btn btn--ghost" href="contact.html">Contact Us</a>
  </div>
  <form class="nf__search" id="nfSearch">
    <input type="search" placeholder="Search the site…" aria-label="Search the site">
    <button class="btn btn--primary" type="submit">Search</button>
  </form>
</div>

<section class="container" style="padding-bottom:26px">
  <div class="cta reveal">
    <span class="cta__icon"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 3 4 6v6c0 5 3.4 8.4 8 9 4.6-.6 8-4 8-9V6z"/></svg></span>
    <div>
      <h3>While you’re here</h3>
      <p>Our most-read guides on business, finance and crypto — all in one place.</p>
    </div>
    <div class="cta__actions">
      <a class="btn btn--light" href="category-business.html">Browse Articles →</a>
    </div>
  </div>
</section>`
  }
];

export default pages;
