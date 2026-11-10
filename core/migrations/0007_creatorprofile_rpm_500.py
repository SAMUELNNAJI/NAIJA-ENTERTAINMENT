from decimal import Decimal

from django.db import migrations, models


def update_default_rpm(apps, schema_editor):
    CreatorProfile = apps.get_model("core", "CreatorProfile")
    CreatorProfile.objects.filter(rpm=Decimal("950.00")).update(rpm=Decimal("500.00"))


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0006_payoutrequest_payout_request_amount_gt_zero"),
    ]

    operations = [
        migrations.RunPython(update_default_rpm, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="creatorprofile",
            name="rpm",
            field=models.DecimalField(
                decimal_places=2,
                default=500,
                help_text="Estimated NGN revenue per 1,000 post views (₦50 per 100 views).",
                max_digits=6,
            ),
        ),
    ]
