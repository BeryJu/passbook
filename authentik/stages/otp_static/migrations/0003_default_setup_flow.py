# Generated by Django 3.1.1 on 2020-09-25 14:32

from django.apps.registry import Apps
from django.db import migrations
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

from authentik.flows.models import FlowDesignation


def create_default_setup_flow(apps: Apps, schema_editor: BaseDatabaseSchemaEditor):
    Flow = apps.get_model("authentik_flows", "Flow")
    FlowStageBinding = apps.get_model("authentik_flows", "FlowStageBinding")

    OTPStaticStage = apps.get_model("authentik_stages_otp_static", "OTPStaticStage")

    db_alias = schema_editor.connection.alias

    flow, _ = Flow.objects.using(db_alias).update_or_create(
        slug="default-otp-static-configure",
        designation=FlowDesignation.STAGE_CONFIGURATION,
        defaults={
            "name": "default-otp-static-configure",
            "title": "Setup Static OTP Tokens",
        },
    )

    stage, _ = OTPStaticStage.objects.using(db_alias).update_or_create(
        name="default-otp-static-configure", defaults={"token_count": 6}
    )

    FlowStageBinding.objects.using(db_alias).update_or_create(
        target=flow, stage=stage, defaults={"order": 0}
    )

    for stage in OTPStaticStage.objects.using(db_alias).filter(configure_flow=None):
        stage.configure_flow = flow
        stage.save()


class Migration(migrations.Migration):

    dependencies = [
        ("authentik_stages_otp_static", "0002_otpstaticstage_configure_flow"),
    ]

    operations = [
        migrations.RunPython(create_default_setup_flow),
    ]
