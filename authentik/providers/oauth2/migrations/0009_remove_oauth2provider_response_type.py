# Generated by Django 3.1.4 on 2020-12-27 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("authentik_providers_oauth2", "0008_oauth2provider_issuer_mode"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="oauth2provider",
            name="response_type",
        ),
    ]
