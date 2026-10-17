"""Forms for signup, login, posts and comments."""
from html.parser import HTMLParser

from django import forms
from django.utils.html import escape
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Comment, PayoutAccount, PayoutRequest, Post, SponsorAd


class BootstrapFormMixin:
    """Apply the site's .field styling to every widget."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault("class", "form-check")
            else:
                widget.attrs.setdefault("class", "field")
            widget.attrs.setdefault("placeholder", field.label or "")


class SignupForm(BootstrapFormMixin, UserCreationForm):
    first_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=True)
    join_as_creator = forms.BooleanField(
        required=False,
        initial=True,
        help_text="Get a creator dashboard, publish blogs and earn from ads.",
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "email")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email


class LoginForm(BootstrapFormMixin, AuthenticationForm):
    """Sign in with a username *or* an email address, in any letter case.

    People routinely type their email address (or retype their username in a
    different case) into the username box, so a plain AuthenticationForm made
    valid accounts — including superusers — look broken on the sign-in page.
    """

    def clean(self):
        username = (self.cleaned_data.get("username") or "").strip()
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(self.request, username=username, password=password)
            if user is None:
                lookup = Q(username__iexact=username)
                if "@" in username:
                    lookup |= Q(email__iexact=username)
                match = User.objects.filter(lookup).order_by("pk").first()
                if match is not None:
                    user = authenticate(
                        self.request, username=match.username, password=password
                    )
            if user is None:
                raise forms.ValidationError(
                    self.error_messages["invalid_login"],
                    code="invalid_login",
                    params={"username": self.username_field.verbose_name},
                )
            if not user.is_active:
                raise forms.ValidationError(
                    self.error_messages["inactive"],
                    code="inactive",
                    params={"username": self.username_field.verbose_name},
                )
            self.user_cache = user
            self.cleaned_data["username"] = user.get_username()
        return self.cleaned_data


class PostForm(BootstrapFormMixin, forms.ModelForm):
    # Optional cover upload — wins over the URL field when both are given.
    cover_upload = forms.FileField(
        required=False,
        label="Cover image upload",
        help_text="JPG, PNG, GIF or WebP up to 5 MB. Overrides the cover URL when provided.",
    )

    class Meta:
        model = Post
        fields = (
            "title",
            "category",
            "tags",
            "image_url",
            "image_alt",
            "excerpt",
            "body",
            "status",
            "is_featured",
            "show_ads",
        )
        widgets = {
            "excerpt": forms.Textarea(attrs={"rows": 3}),
            "body": forms.Textarea(attrs={"rows": 14}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = user
        # The cover can be provided as a URL *or* an upload; clean() enforces
        # that at least one of them is present.
        self.fields["image_url"].required = False
        # Only staff may feature posts or toggle ads.
        if user is None or not user.is_staff:
            self.fields.pop("is_featured", None)

    def clean_cover_upload(self):
        upload = self.cleaned_data.get("cover_upload")
        if upload:
            if upload.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Cover images must be 5 MB or smaller.")
            ext = upload.name.rsplit(".", 1)[-1].lower()
            if ext not in ("jpg", "jpeg", "png", "gif", "webp"):
                raise forms.ValidationError("Use a JPG, PNG, GIF or WebP image.")
        return upload

    def clean(self):
        cleaned = super().clean()
        # A cover is required unless the creator is uploading one instead.
        if not (cleaned.get("image_url") or "").strip() and not cleaned.get(
            "cover_upload"
        ):
            self.add_error("image_url", "Add a cover image URL or upload an image.")
        return cleaned

    def clean_body(self):
        """Keep editor markup while rejecting executable HTML."""
        allowed_tags = {"a", "blockquote", "br", "code", "div", "em", "h2", "h3", "li", "ol", "p", "pre", "strong", "u", "ul"}
        allowed_attrs = {"a": {"href", "title", "target", "rel"}}

        class SafeHTML(HTMLParser):
            def __init__(self):
                super().__init__(convert_charrefs=True)
                self.parts = []

            def handle_starttag(self, tag, attrs):
                if tag not in allowed_tags:
                    return
                safe = []
                for key, value in attrs:
                    if key not in allowed_attrs.get(tag, set()) or value is None:
                        continue
                    if key == "href" and not value.lower().startswith(("https://", "http://", "mailto:", "/", "#")):
                        continue
                    safe.append(f' {key}="{escape(value)}"')
                self.parts.append(f"<{tag}{''.join(safe)}>")

            def handle_endtag(self, tag):
                if tag in allowed_tags and tag != "br":
                    self.parts.append(f"</{tag}>")

            def handle_data(self, data):
                self.parts.append(escape(data))

        parser = SafeHTML()
        parser.feed(self.cleaned_data["body"])
        parser.close()
        return "".join(parser.parts).strip()


class CommentForm(BootstrapFormMixin, forms.ModelForm):
    # Readers can comment from the compact article form, which intentionally
    # collects only their message.  Authenticated users keep their account
    # name; guests are shown as "Guest" by the create view.
    name = forms.CharField(max_length=120, required=False)

    class Meta:
        model = Comment
        fields = ("name", "email", "body")
        widgets = {"body": forms.Textarea(attrs={"rows": 3})}


class PayoutAccountForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = PayoutAccount
        fields = ("bank_name", "account_name", "account_number")


class PayoutRequestForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = PayoutRequest
        fields = ("amount",)


class SponsorAdForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = SponsorAd
        fields = ("title", "image_url", "redirect_url", "is_active")
