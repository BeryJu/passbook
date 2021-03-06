"""authentik events NotificationTransport forms"""
from django import forms
from django.utils.translation import gettext_lazy as _

from authentik.events.models import NotificationRule, NotificationTransport


class NotificationTransportForm(forms.ModelForm):
    """NotificationTransport Form"""

    class Meta:

        model = NotificationTransport
        fields = [
            "name",
            "mode",
            "webhook_url",
        ]
        widgets = {
            "name": forms.TextInput(),
            "webhook_url": forms.TextInput(),
        }
        labels = {
            "webhook_url": _("Webhook URL"),
        }
        help_texts = {
            "webhook_url": _(
                ("Only required when the Generic or Slack Webhook is used.")
            ),
        }


class NotificationRuleForm(forms.ModelForm):
    """NotificationRule Form"""

    class Meta:

        model = NotificationRule
        fields = [
            "name",
            "group",
            "transports",
            "severity",
        ]
        widgets = {
            "name": forms.TextInput(),
        }
