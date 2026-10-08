# The Nigerian Entrepreneur — static site

A hand-built HTML / CSS / JavaScript replication of the designs supplied as
screenshots. No frameworks and no build step needed to view it — open
`home/index.html` in a browser.

## Layout — one directory per page

```
home/                                  Homepage
services/                              Our Services
about/                                 About Us
contact/                               Contact Us
privacy-policy/                        Privacy Policy
404/                                   Page Not Found
finance/                               Finance archive
business/                              Business archive
crypto/                                Crypto / Web 3.0 archive
entrepreneur/                          Entrepreneur Corner archive
affiliates/                            Affiliates archive
article-10-profitable-business-ideas/  Full article page

assets/
  css/style.css                        single stylesheet (tokens + components)
  js/main.js                           all behaviour, vanilla JS
  img/*.svg                            illustrations that replace the photos

reference/                             the 7 original design screenshots
tools/                                 optional page generator
```

Each page is `index.html` inside its own folder, so all cross-page links go
through `../` (e.g. `../finance/index.html`) and shared assets through
`../assets/...`.

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
files, edit `home/index.html` (it is the shell) and re-run:

```bash
node tools/build.mjs
```

`tools/content-categories.mjs` and `tools/content-pages.mjs` hold the page
bodies; `tools/build.mjs` merges them with the shell and rewrites every
root-relative URL for the one-directory-deep layout (idempotent, so running it
twice is safe).

The generated `.html` files are plain static files — you can also edit them by
hand and simply not run the generator again. Only re-run it after changing the
header or footer in `home/index.html`.
