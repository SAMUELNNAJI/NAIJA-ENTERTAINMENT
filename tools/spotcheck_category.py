import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
os.environ.setdefault("DJANGO_ALLOWED_HOSTS", "testserver")

import django

django.setup()

from django.test import Client

client = Client()
body = client.get("/category/finance/").content.decode()

checks = {
    "feature card": body.count("feature-card feature-card--spotlight") == 1,
    # DB-driven library: one spotlight + fourteen mini cards (4 beside the
    # feature, 10 behind Load more) = the fifteen-article category page.
    "mini cards (4 stack + 10 more)": body.count('class="mini-card reveal"') == 14,
    "hidden load-more items": body.count("data-more-item hidden") == 10,
    # Chips are real links now: All + five ?filter= chips in the filter bar.
    "filter chips (6, as links)": body.count('class="chip') == 6,
    "chip links use ?filter=": len(
        re.findall(r'<a class="chip[^"]*" href="/category/finance/\?filter=', body)
    ) == 5,
    # hero + feature + 14 mini cards + 3 logo placements (covers are mostly
    # remote URLs now, so count every rendered image instead of /static only)
    "card images": len(re.findall(r"<img ", body)) == 19,
    "subscribe CTA form": "cta__form" in body,
    "hero theme": "page-hero t-finance" in body,
    "load-more button": "data-more-btn" in body,
    "empty state": "data-empty" in body,
}

ok = True
for name, passed in checks.items():
    print(f"{'OK ' if passed else 'FAIL'}  {name}")
    ok = ok and passed

sys.exit(0 if ok else 1)
