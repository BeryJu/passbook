# Generated by Django 3.1.1 on 2020-09-21 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentik_events", "0003_auto_20200917_1155"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="action",
            field=models.TextField(
                choices=[
                    ("login", "Login"),
                    ("login_failed", "Login Failed"),
                    ("logout", "Logout"),
                    ("sign_up", "Sign Up"),
                    ("authorize_application", "Authorize Application"),
                    ("suspicious_request", "Suspicious Request"),
                    ("password_set", "Password Set"),
                    ("invitation_created", "Invite Created"),
                    ("invitation_used", "Invite Used"),
                    ("source_linked", "Source Linked"),
                    ("impersonation_started", "Impersonation Started"),
                    ("impersonation_ended", "Impersonation Ended"),
                    ("model_created", "Model Created"),
                    ("model_updated", "Model Updated"),
                    ("model_deleted", "Model Deleted"),
                    ("custom_", "Custom Prefix"),
                ]
            ),
        ),
    ]
