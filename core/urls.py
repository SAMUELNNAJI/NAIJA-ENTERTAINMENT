from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from . import views, views_dashboard, views_tools

from .forms import CustomPasswordResetForm, CustomSetPasswordForm

urlpatterns = [
    path("", views.home, name="home"),
    # site-wide search
    path("search/", views.search, name="search"),
    # blog
    re_path(r"^blog/(?P<slug>[\w-]+)/$", views.blog_detail, name="blog_detail"),
    # comments (AJAX)
    re_path(
        r"^blog/(?P<slug>[\w-]+)/comment/$",
        views.comment_create,
        name="comment_create",
    ),
    path("comment/<int:pk>/edit/", views.comment_edit, name="comment_edit"),
    path("comment/<int:pk>/delete/", views.comment_delete, name="comment_delete"),
    # auth
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            form_class=CustomPasswordResetForm,
            template_name="auth/password_reset.html",
            email_template_name="auth/password_reset_email.html",
            subject_template_name="auth/password_reset_subject.txt",
            success_url="/password-reset/done/",
        ),
    ),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            form_class=CustomPasswordResetForm,
            template_name="auth/password_reset.html",
            email_template_name="auth/password_reset_email.html",
            subject_template_name="auth/password_reset_subject.txt",
            success_url="/password-reset/done/",
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="auth/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            form_class=CustomSetPasswordForm,
            template_name="auth/password_reset_confirm.html",
            success_url="/password-reset/complete/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="auth/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="auth/password_reset_complete.html"
        ),
    ),
    path("subscribe/", views.subscribe, name="subscribe"),
    # dashboards
    path("dashboard/", views_dashboard.dashboard, name="dashboard"),
    path("dashboard/posts/", views_dashboard.dashboard_posts, name="dashboard_posts"),
    path("dashboard/payouts/", views_dashboard.payouts, name="payouts"),
    path("dashboard/post/new/", views_dashboard.dashboard_post_new, name="dashboard_post_new"),
    path(
        "dashboard/post/<int:pk>/edit/",
        views_dashboard.dashboard_post_edit,
        name="dashboard_post_edit",
    ),
    path(
        "dashboard/post/<int:pk>/delete/",
        views_dashboard.dashboard_post_delete,
        name="dashboard_post_delete",
    ),
    # admin control panel (staff)
    path("panel/", views_dashboard.admin_panel, name="admin_panel"),
    path("panel/posts/", views_dashboard.admin_panel_posts, name="admin_panel_posts"),
    path("panel/posts/new/", views_dashboard.admin_panel_post_new, name="admin_panel_post_new"),
    path("panel/post/<int:pk>/edit/", views_dashboard.admin_panel_post_edit, name="admin_panel_post_edit"),
    path(
        "panel/post/<int:pk>/toggle/",
        views_dashboard.admin_panel_toggle_publish,
        name="admin_panel_toggle_publish",
    ),
    path(
        "panel/post/<int:pk>/delete/",
        views_dashboard.admin_panel_post_delete,
        name="admin_panel_post_delete",
    ),
    path("panel/comments/", views_dashboard.admin_panel_comments, name="admin_panel_comments"),
    path("panel/users/", views_dashboard.admin_panel_users, name="admin_panel_users"),
    path(
        "panel/user/<int:pk>/toggle-suspend/",
        views_dashboard.admin_panel_user_toggle_suspend,
        name="admin_panel_user_toggle_suspend",
    ),
    path(
        "panel/user/<int:pk>/delete/",
        views_dashboard.admin_panel_user_delete,
        name="admin_panel_user_delete",
    ),
    path(
        "notification/<int:pk>/dismiss/",
        views_dashboard.notification_dismiss,
        name="notification_dismiss",
    ),
    path("panel/payouts/", views_dashboard.admin_panel_payouts, name="admin_panel_payouts"),
    path("panel/sponsors/", views_dashboard.admin_panel_sponsors, name="admin_panel_sponsors"),
    path("panel/sponsor/<int:pk>/toggle/", views_dashboard.admin_panel_sponsor_toggle, name="admin_panel_sponsor_toggle"),
    path("panel/sponsor/<int:pk>/edit/", views_dashboard.admin_panel_sponsor_edit, name="admin_panel_sponsor_edit"),
    path("panel/post/<int:pk>/featured/", views_dashboard.admin_panel_toggle_featured, name="admin_panel_toggle_featured"),
    path("panel/payout/<int:pk>/<str:action>/", views_dashboard.admin_panel_payout_action, name="admin_panel_payout_action"),
    path(
        "panel/comment/<int:pk>/toggle/",
        views_dashboard.admin_panel_comment_toggle,
        name="admin_panel_comment_toggle",
    ),
    # tools
    path("tools/currency/", views_tools.currency_converter, name="currency_converter"),
    path("tools/currency/rates/", views_tools.currency_rates, name="currency_rates"),
    path("markets/", views_tools.markets, name="markets"),
    path("markets/snapshot/", views_tools.market_snapshot, name="market_snapshot"),
    # category archives: /finance/, /business/, /crypto/, ...
    re_path(r"^category/(?P<slug>[\w-]+)/$", views.category, name="category"),
    # long-form articles: /article/<slug>/
    re_path(r"^article/(?P<slug>[\w-]+)/$", views.article, name="article"),
    # simple static pages: /about/, /contact/, /services/, /privacy-policy/
    re_path(r"^(?P<slug>[\w-]+)/$", views.page, name="page"),
]

