# The Nigerian Entrepreneur — static site

A hand-built HTML / CSS / JavaScript replication of the designs supplied as
screenshots in the project root. No frameworks, no build step required to view
it — open `index.html` in a browser.

## Pages

| File | Purpose |
| --- | --- |
| `index.html` | Homepage — hero, category cards, featured articles, sidebar widgets, CTA |
| `services.html` | Our Services — six service cards + support CTA |
| `about.html` | About Us — logo block, Who We Are, Our Vision, what we cover |
| `contact.html` | Contact Us — validated message form + contact details sidebar |
| `privacy-policy.html` | Privacy Policy — sticky table of contents + numbered sections |
| `404.html` | Page Not Found |
| `finance.html` | Finance archive |
| `business.html` | Business archive |
| `crypto.html` | Crypto / Web 3.0 archive |
| `entrepreneur.html` | Entrepreneur Corner archive |
| `affiliates.html` | Affiliates archive |
| `article-10-profitable-business-ideas.html` | Full article with table of contents and share row |

## Assets

```
assets/css/style.css   single stylesheet (design tokens + all components)
assets/js/main.js      all behaviour, vanilla JS
assets/img/*.svg       illustrations that replace the photos in the screenshots
tools/                 optional page generator (see below)
```

## Behaviour (assets/js/main.js)

- Sticky header with hover dropdowns on desktop, accordion drawer on mobile
- Search panel drawer (`#searchToggle`)
- Category filter chips — filters the article list by tag, with an empty state
- "Load more articles" — reveals the remaining hidden entries, then removes itself
- Newsletter + contact form validation with inline status messages and a toast
- `data-copy-link` copy-link button, scroll-spy for the privacy/article TOCs
- IntersectionObserver reveal animations with a safety net so content is never
  left hidden, plus `prefers-reduced-motion` and print fallbacks
- Back-to-top button, auto footer year

## Optional page generator

Every page shares one header and footer. If you need to change them across all
files, edit `index.html` (it is the shell) and re-run:

```bash
node tools/build.mjs
```

`tools/content-categories.mjs` and `tools/content-pages.mjs` hold the page
bodies; `tools/build.mjs` merges them with the shell. The generated `.html`
files are plain static files — you can also edit them by hand and simply not
run the generator again.
