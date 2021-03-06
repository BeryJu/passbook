# Generated by Django 3.0.8 on 2020-07-08 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentik_sources_saml", "0004_auto_20200708_1207"),
    ]

    operations = [
        migrations.AddField(
            model_name="samlsource",
            name="name_id_policy",
            field=models.TextField(
                choices=[
                    ("urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress", "Email"),
                    (
                        "urn:oasis:names:tc:SAML:2.0:nameid-format:persistent",
                        "Persistent",
                    ),
                    (
                        "urn:oasis:names:tc:SAML:2.0:nameid-format:X509SubjectName",
                        "X509",
                    ),
                    (
                        "urn:oasis:names:tc:SAML:2.0:nameid-format:WindowsDomainQualifiedName",
                        "Windows",
                    ),
                    (
                        "urn:oasis:names:tc:SAML:2.0:nameid-format:transient",
                        "Transient",
                    ),
                ],
                default="urn:oasis:names:tc:SAML:2.0:nameid-format:transient",
                help_text="NameID Policy sent to the IdP. Can be unset, in which case no Policy is sent.",
            ),
        ),
    ]
