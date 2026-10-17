from .models import SponsorAd


def active_sponsor_ads(request):
    return {"sponsor_ads": SponsorAd.objects.filter(is_active=True)[:20]}
