"""Django admin for The Nigerian Entrepreneur."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Comment, CreatorProfile, NewsletterSubscriber, Post, PostDailyStat


class CreatorProfileInline(admin.StackedInline):
    model = CreatorProfile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = [CreatorProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "author", "views", "published_at")
    list_filter = ("status", "category", "is_featured")
    search_fields = ("title", "excerpt", "body")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "post", "is_approved", "created_at")
    list_filter = ("is_approved",)
    search_fields = ("name", "email", "body")


admin.site.register([PostDailyStat, NewsletterSubscriber])
