# Generated by Django 3.1.2 on 2020-10-03 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("authentik_core", "0011_provider_name_temp"),
        ("authentik_providers_oauth2", "0006_remove_oauth2provider_name"),
        ("authentik_providers_saml", "0006_remove_samlprovider_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="provider",
            old_name="name_temp",
            new_name="name",
        ),
    ]
