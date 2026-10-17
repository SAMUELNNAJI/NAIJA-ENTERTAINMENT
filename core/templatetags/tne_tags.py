"""Custom template filters for TNE.

``tojson`` serialises a Python value into valid, double-quoted JSON so it can
be safely embedded in ``data-*`` attributes or ``<script type="application/json">`` blocks.
"""
import json

from django import template

register = template.Library()


@register.filter
def tojson(value):
    return json.dumps(value)


@register.filter
def friendly(value):
    """Human-relative date, e.g. '3 days ago'."""
    from django.utils import timezone
    from django.utils.timesince import timesince

    if not value:
        return ""
    return f"{timesince(value)} ago"
