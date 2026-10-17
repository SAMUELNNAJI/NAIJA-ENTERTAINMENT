"""
Bootstrap Django templates from the legacy flat static pages.

ONE-OFF conversion helper (kept for traceability). It was used to create the
initial Django templates from the generated static HTML files:

  - templates/base.html       built from the <head>, <header> and <footer> of
                              index.html (the shell), with {% block %}s and
                              nav_active conditionals added.
  - templates/pages/<page>.html  built from the <main> body of each page, with
                              assets/... rewritten to {% static '...' %} and
                              internal *.html links rewritten to {% url %}.

Re-running it overwrites the generated templates. The category archive page
(templates/pages/category.html + templates/includes/*) is hand-maintained
and is NOT produced by this script.

Usage:
    python tools/extract_django_templates.py
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates"

# legacy page file -> (template path, page_id)
PAGES = {
    "index.html": ("pages/home.html", "home"),
    "services.html": ("pages/services.html", "services"),
    "about.html": ("pages/about.html", "about"),
    "contact.html": ("pages/contact.html", "contact"),
    "privacy-policy.html": ("pages/privacy_policy.html", "privacy-policy"),
    "article-10-profitable-business-ideas.html": ("pages/article.html", "article"),
    "404.html": ("pages/404.html", "404"),
}

# legacy internal link -> (url name, url arg or None)
LINKS = {
    "index.html": ("home", None),
    "about.html": ("page", "about"),
    "contact.html": ("page", "contact"),
    "services.html": ("page", "services"),
    "privacy-policy.html": ("page", "privacy-policy"),
    "finance.html": ("category", "finance"),
    "business.html": ("category", "business"),
    "crypto.html": ("category", "crypto"),
    "entrepreneur.html": ("category", "entrepreneur"),
    "affiliates.html": ("category", "affiliates"),
    "category-finance.html": ("category", "finance"),
    "category-business.html": ("category", "business"),
    "category-crypto.html": ("category", "crypto"),
    "category-entrepreneur.html": ("category", "entrepreneur"),
    "category-affiliates.html": ("category", "affiliates"),
    "article-10-profitable-business-ideas.html": (
        "article",
        "10-profitable-business-ideas",
    ),
}


def url_tag(name: str, arg: str | None) -> str:
    if arg:
        return "{%% url '%s' '%s' %%}" % (name, arg)
    return "{%% url '%s' %%}" % name


def rewrite(html: str) -> str:
    """assets/... -> {% static %} and internal .html links -> {% url %}."""

    def repl(match: re.Match) -> str:
        attr, url = match.group(1), match.group(2)
        if url.startswith(("http:", "https:", "mailto:", "tel:", "#", "/", "{%")):
            return match.group(0)

        if url.startswith("assets/"):
            return '%s="{%% static \'%s\' %%}"' % (attr, url[len("assets/") :])

        file, _, hash_ = url.partition("#")
        if file in LINKS:
            name, arg = LINKS[file]
            suffix = f"#{hash_}" if hash_ else ""
            return '%s="%s%s"' % (attr, url_tag(name, arg), suffix)
        return match.group(0)

    return re.sub(r'(href|src)="([^"]+)"', repl, html)


def extract(html: str, pattern: str, label: str) -> str:
    match = re.search(pattern, html, re.S)
    if not match:
        raise SystemExit(f"Could not extract {label}")
    return match.group(1)


def add_active_nav(header: str) -> str:
    """Turn the static header into one that marks the active nav entry."""
    header = rewrite(header)

    # direct link (Crypto / Web 3.0)
    crypto = '<li class="nav__item"><a href="{% url \'category\' \'crypto\' %}">'
    header = header.replace(
        crypto,
        "<li class=\"nav__item{% if nav_active == 'crypto' %} is-active{% endif %}\">"
        '<a href="{% url \'category\' \'crypto\' %}">',
    )

    # dropdown parents — activate the <li> that contains the trigger
    has_menu = '<li class="nav__item has-menu">'
    for key, trigger in [
        ("finance", "Finance <i"),
        ("business", "Business <i"),
        ("entrepreneur", "Entrepreneur Corner <i"),
        ("affiliate", "Affiliates <i"),
        ("more", "More <i"),
    ]:
        pos = header.index(trigger)
        li_pos = header.rfind(has_menu, 0, pos)
        if li_pos == -1:
            raise SystemExit(f"Could not find nav item for {key!r}")
        conditional = (
            '<li class="nav__item has-menu'
            + "{%% if nav_active == '%s' %%} is-active{%% endif %%}" % key
            + '">'
        )
        header = header[:li_pos] + conditional + header[li_pos + len(has_menu) :]
    return header


def build_base(shell: str) -> str:
    head_inner = extract(shell, r"<head>([\s\S]*?)</head>", "head inner")
    title = extract(shell, r"<title>([\s\S]*?)</title>", "title").strip()
    description = extract(
        shell, r'<meta name="description" content="([^"]*)">', "description"
    )
    header = extract(
        shell,
        r'(<a class="btn btn--primary btn--sm" href="#main"[\s\S]*?</header>)',
        "header",
    )
    footer = extract(shell, r"(<footer class=\"site-footer\">[\s\S]*)", "footer")

    head_inner = re.sub(r"\s*<title>[\s\S]*?</title>", "", head_inner)
    head_inner = re.sub(r'\s*<meta name="description"[^>]*>', "", head_inner)
    head_inner = re.sub(r'\s*<link rel="stylesheet"[^>]*>', "", head_inner)
    head_inner = head_inner.replace(
        'href="assets/img/photos/LOgo.png"',
        'href="{% static \'img/photos/LOgo.png\' %}"',
    )
    head_inner = rewrite(head_inner).strip()

    header = add_active_nav(header)
    footer = rewrite(footer)
    footer = footer.replace("</body>", "{% block scripts %}{% endblock %}\n</body>", 1)

    return (
        "{% load static %}\n"
        "<!DOCTYPE html>\n"
        '<html lang="en">\n'
        "<head>\n"
        + head_inner
        + "\n"
        + "<title>{%% block title %%}%s{%% endblock %%}</title>\n" % title
        + '<meta name="description" content="{%% block meta_description %%}%s{%% endblock %%}">\n' % description
        + '<link rel="stylesheet" href="{% static \'css/style.css\' %}">\n'
        + "{% block extra_head %}{% endblock %}\n"
        + "</head>\n"
        + '<body data-page="{% block page_id %}page{% endblock %}">\n\n'
        + header
        + "\n\n"
        + '<main id="main">\n'
        + "{% block content %}{% endblock %}\n"
        + "</main>\n\n"
        + footer
    )


def build_page(html: str, page_id: str) -> str:
    title = extract(html, r"<title>([\s\S]*?)</title>", "title").strip()
    description = extract(
        html, r'<meta name="description" content="([^"]*)">', "description"
    )
    body = rewrite(extract(html, r'<main id="main">\s*([\s\S]*?)\s*</main>', "main"))

    load = "{% load static %}\n" if "{% static" in body else ""
    return (
        '{% extends "base.html" %}\n'
        + load
        + "\n"
        + "{%% block title %%}%s{%% endblock %%}\n" % title
        + '{%% block meta_description %%}%s{%% endblock %%}\n' % description
        + "{%% block page_id %%}%s{%% endblock %%}\n" % page_id
        + "\n"
        + "{% block content %}\n"
        + body
        + "\n{% endblock %}\n"
    )


def main() -> None:
    shell = (ROOT / "index.html").read_text(encoding="utf-8").replace("\r\n", "\n")

    (TEMPLATES / "pages").mkdir(parents=True, exist_ok=True)
    (TEMPLATES / "base.html").write_text(build_base(shell), encoding="utf-8")
    print("wrote templates/base.html")

    for file, (template, page_id) in PAGES.items():
        html = (ROOT / file).read_text(encoding="utf-8").replace("\r\n", "\n")
        out = TEMPLATES / template
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(build_page(html, page_id), encoding="utf-8")
        print(f"wrote templates/{template}")


if __name__ == "__main__":
    main()


