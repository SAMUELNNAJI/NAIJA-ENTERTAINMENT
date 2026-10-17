from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("core", "0002_payouts")]
    operations = [migrations.CreateModel(name="SponsorAd", fields=[
        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
        ("title", models.CharField(max_length=140)),
        ("image_url", models.CharField(help_text="Image URL or path under assets/.", max_length=500)),
        ("redirect_url", models.URLField(help_text="Where the banner opens when clicked.")),
        ("is_active", models.BooleanField(default=True)),
        ("created_at", models.DateTimeField(auto_now_add=True)),
    ], options={"ordering": ["-created_at"]})]
