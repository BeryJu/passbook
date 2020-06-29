# Generated by Django 3.0.6 on 2020-05-24 11:34

from django.apps.registry import Apps
from django.db import migrations
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

from passbook.flows.models import FlowDesignation


def create_default_provider_authorization_flow(
    apps: Apps, schema_editor: BaseDatabaseSchemaEditor
):
    Flow = apps.get_model("passbook_flows", "Flow")
    FlowStageBinding = apps.get_model("passbook_flows", "FlowStageBinding")

    ConsentStage = apps.get_model("passbook_stages_consent", "ConsentStage")

    db_alias = schema_editor.connection.alias

    # Empty flow for providers where consent is implicitly given
    Flow.objects.using(db_alias).update_or_create(
        slug="default-provider-authorization-implicit-consent",
        designation=FlowDesignation.AUTHORIZATION,
        defaults={"name": "Authorize Application"},
    )

    # Flow with consent form to obtain explicit user consent
    flow, _ = Flow.objects.using(db_alias).update_or_create(
        slug="default-provider-authorization-explicit-consent",
        designation=FlowDesignation.AUTHORIZATION,
        defaults={"name": "Authorize Application"},
    )
    stage, _ = ConsentStage.objects.using(db_alias).update_or_create(
        name="default-provider-authorization-consent"
    )
    FlowStageBinding.objects.using(db_alias).update_or_create(
        flow=flow, stage=stage, defaults={"order": 0}
    )


class Migration(migrations.Migration):

    dependencies = [
        ("passbook_flows", "0004_source_flows"),
        ("passbook_stages_consent", "0001_initial"),
    ]

    operations = [migrations.RunPython(create_default_provider_authorization_flow)]
