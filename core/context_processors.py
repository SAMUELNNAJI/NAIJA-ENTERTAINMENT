from django.urls import resolve

from .models import SponsorAd

NO_AD_URL_NAMES = {
    # Auth
    "login", "signup", "logout",
    "password_reset", "password_reset_done", "password_reset_confirm", "password_reset_complete",
    # Dashboard / admin panel
    "dashboard", "dashboard_posts", "dashboard_payouts", "dashboard_post_new",
    "dashboard_post_edit", "dashboard_post_delete",
    "admin_panel", "admin_panel_posts", "admin_panel_post_new", "admin_panel_post_edit",
    "admin_panel_toggle_publish", "admin_panel_post_delete", "admin_panel_comments",
    "admin_panel_users", "admin_panel_user_toggle_suspend", "admin_panel_user_delete",
    "notification_dismiss", "admin_panel_payouts", "admin_panel_sponsors",
    "admin_panel_sponsor_toggle", "admin_panel_sponsor_edit", "admin_panel_toggle_featured",
    "admin_panel_payout_action", "admin_panel_comment_toggle",
    # Tools
    "currency_converter", "currency_rates", "markets", "market_snapshot",
}


def active_sponsor_ads(request):
    return {"sponsor_ads": SponsorAd.objects.filter(is_active=True)[:20]}


def show_ads(request):
    try:
        url_name = resolve(request.path_info).url_name
    except Exception:
        url_name = ""
    return {"show_ads": url_name not in NO_AD_URL_NAMES}
