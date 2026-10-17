from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("core", "0001_initial")]
    operations = [
        migrations.CreateModel(name="PayoutAccount", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("bank_name", models.CharField(max_length=120)), ("account_name", models.CharField(max_length=120)),
            ("account_number", models.CharField(max_length=20)), ("updated_at", models.DateTimeField(auto_now=True)),
            ("creator", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="payout_account", to="core.creatorprofile")),
        ]),
        migrations.CreateModel(name="PayoutRequest", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("amount", models.DecimalField(decimal_places=2, max_digits=12)),
            ("status", models.CharField(choices=[("pending", "Pending"), ("paid", "Paid"), ("rejected", "Rejected")], default="pending", max_length=10)),
            ("note", models.CharField(blank=True, max_length=500)), ("created_at", models.DateTimeField(auto_now_add=True)), ("processed_at", models.DateTimeField(blank=True, null=True)),
            ("account", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="requests", to="core.payoutaccount")),
            ("creator", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="payout_requests", to="core.creatorprofile")),
        ]),
    ]
