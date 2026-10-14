/**
 * Static site generator for "The Nigerian Entrepreneur".
 *
 * index.html is the shell: its <head>, header and footer are extracted
 * once and reused for every other page, so navigation stays identical
 * site-wide. Page bodies live in ./content-*.mjs.
 *
 * Every page lives in its own directory at the project root, so all links are
 * written once, root-relative, and rebased here:
 *   assets/...            -> ../assets/...
 *   category-finance.html -> finance.html
 *
 *   node tools/build.mjs
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SHELL = 'index.html';
const shell = fs.readFileSync(path.join(root, SHELL), 'utf8');

/* page name (as authored) -> directory it lives in */
const ROUTES = {
  'index.html': 'index.html',
  'services.html': 'services.html',
  'about.html': 'about.html',
  'contact.html': 'contact.html',
  'privacy-policy.html': 'privacy-policy.html',
  '404.html': '404.html',
  'category-finance.html': 'finance.html',
  'category-business.html': 'business.html',
  'category-crypto.html': 'crypto.html',
  'category-entrepreneur.html': 'entrepreneur.html',
  'category-affiliates.html': 'affiliates.html',
  'article-10-profitable-business-ideas.html': 'article-10-profitable-business-ideas.html'
};

/* which nav entry each content section belongs to */
const HEADER_LINKS = {
  finance: 'category-finance.html',
  business: 'category-business.html',
  crypto: 'category-crypto.html',
  startup: 'category-entrepreneur.html',
  affiliate: 'category-affiliates.html'
};

/** Pages sit flat at the project root, so routes are plain file names. */
const routeUrl = (file) => ROUTES[file];
const ROUTE_FILES = new Set(Object.values(ROUTES));

/**
 * Rewrites root-relative URLs for pages that live in their own directory.
 * Idempotent — already-rebased URLs are left alone.
 */
export function rebase(html) {
  return html.replace(/(href|src)="([^"]+)"/g, (match, attr, url) => {
    if (/^(https?:|mailto:|tel:|#|\.\.\/)/.test(url)) return match;

    const hashAt = url.indexOf('#');
    const file = hashAt === -1 ? url : url.slice(0, hashAt);
    const hash = hashAt === -1 ? '' : url.slice(hashAt);

    if (file.startsWith('assets/')) return match;
    if (ROUTES[file]) return `${attr}="${routeUrl(file)}${hash}"`;
    if (ROUTE_FILES.has(file)) return match;
    return match;
  });
}

/* ---------- extract reusable pieces from the shell page ---------- */
/**
 * Copies shell text from `from` up to `to`.
 * `to` is exclusive by default; pass { inclusive: true } to keep the marker
 * itself. The header needs this: dropping `</header>` would leave <main>,
 * <footer>, .to-top and .toast nested inside <header>, which breaks the
 * sticky positioning and the dropdown stacking.
 */
const slice = (from, to, { inclusive = false } = {}) => {
  const a = shell.indexOf(from);
  const b = shell.indexOf(to, a);
  if (a === -1 || b === -1) throw new Error(`Could not extract "${from}" from ${SHELL}`);
  return shell.slice(a, inclusive ? b + to.length : b);
};

const head = slice('<!DOCTYPE html>', '<link rel="stylesheet"').trim();
const header = slice('<a class="btn btn--primary btn--sm" href="#main"', '</header>', { inclusive: true });
const footer = slice('<footer class="site-footer">', '</html>');

/** Marks the matching nav entry (or its dropdown parent) as active. */
function markActive(html, active) {
  if (!active || active === 'home') return html;
  const href = HEADER_LINKS[active];
  if (!href) return html;

  // tries the authored name, then the rebased path
  for (const target of [href, ROUTES[href], routeUrl(href)]) {
    // direct link (Crypto / Web 3.0)
    const direct = `<li class="nav__item"><a href="${target}">`;
    if (html.includes(direct)) {
      return html.replace(direct, `<li class="nav__item is-active"><a href="${target}">`);
    }

    // dropdown parent — activate the <li> that contains the link
    const liStart = html.lastIndexOf('<li class="nav__item has-menu">', html.indexOf(`"${target}"`));
    if (liStart !== -1) {
      return (
        html.slice(0, liStart) +
        '<li class="nav__item has-menu is-active">' +
        html.slice(liStart + '<li class="nav__item has-menu">'.length)
      );
    }
  }
  return html;
}

function render({ file, title, description, page, active, body }) {
  const pageHead = head
    .replace(/<title>[\s\S]*?<\/title>/, `<title>${title}</title>`)
    .replace(/\s*<meta name="description"[^>]*>/, '');

  const doc = `${pageHead}
  <meta name="description" content="${description}">
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body data-page="${page}">

${markActive(header, active)}

<main id="main">
${body.trim()}
</main>

${footer.trim()}
`;

  const out = path.join(root, ROUTES[file] ?? file);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, rebase(doc));
  return ROUTES[file] ?? file;
}

/* ---------- build ---------- */
if (process.argv.includes('--rebase')) {
  fs.writeFileSync(path.join(root, SHELL), rebase(fs.readFileSync(path.join(root, SHELL), 'utf8')));
  console.log(`Rebased ${SHELL} for its new location.`);
}

const groups = [];
for (const mod of ['./content-categories.mjs', './content-pages.mjs']) {
  groups.push(...(await import(mod)).default);
}

const written = groups.map(render);
console.log(`Built ${written.length} pages from ${SHELL}:\n  ` + written.join('\n  '));
