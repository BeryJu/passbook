# Generated by Django 3.1.4 on 2020-12-27 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentik_stages_invitation", "0002_auto_20201225_2143"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invitation",
            name="fixed_data",
            field=models.JSONField(
                blank=True,
                default=dict,
                help_text="Optional fixed data to enforce on user enrollment.",
            ),
        ),
    ]
