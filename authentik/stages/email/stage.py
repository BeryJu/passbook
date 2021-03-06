"""authentik multi-stage authentication engine"""
from datetime import timedelta

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, reverse
from django.utils.http import urlencode
from django.utils.timezone import now
from django.utils.translation import gettext as _
from django.views.generic import FormView
from structlog.stdlib import get_logger

from authentik.core.models import Token
from authentik.flows.planner import PLAN_CONTEXT_PENDING_USER
from authentik.flows.stage import StageView
from authentik.flows.views import SESSION_KEY_GET
from authentik.stages.email.forms import EmailStageSendForm
from authentik.stages.email.models import EmailStage
from authentik.stages.email.tasks import send_mails
from authentik.stages.email.utils import TemplateEmailMessage

LOGGER = get_logger()
QS_KEY_TOKEN = "token"  # nosec
PLAN_CONTEXT_EMAIL_SENT = "email_sent"


class EmailStageView(FormView, StageView):
    """Email stage which sends Email for verification"""

    form_class = EmailStageSendForm
    template_name = "stages/email/waiting_message.html"

    def get_full_url(self, **kwargs) -> str:
        """Get full URL to be used in template"""
        base_url = reverse(
            "authentik_flows:flow-executor-shell",
            kwargs={"flow_slug": self.executor.flow.slug},
        )
        relative_url = f"{base_url}?{urlencode(kwargs)}"
        return self.request.build_absolute_uri(relative_url)

    def send_email(self):
        """Helper function that sends the actual email. Implies that you've
        already checked that there is a pending user."""
        pending_user = self.executor.plan.context[PLAN_CONTEXT_PENDING_USER]
        current_stage: EmailStage = self.executor.current_stage
        valid_delta = timedelta(
            minutes=current_stage.token_expiry + 1
        )  # + 1 because django timesince always rounds down
        token = Token.objects.create(user=pending_user, expires=now() + valid_delta)
        # Send mail to user
        message = TemplateEmailMessage(
            subject=_(current_stage.subject),
            template_name=current_stage.template,
            to=[pending_user.email],
            template_context={
                "url": self.get_full_url(**{QS_KEY_TOKEN: token.pk.hex}),
                "user": pending_user,
                "expires": token.expires,
            },
        )
        send_mails(current_stage, message)

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        # Check if the user came back from the email link to verify
        if QS_KEY_TOKEN in request.session.get(SESSION_KEY_GET, {}):
            token = get_object_or_404(
                Token, pk=request.session[SESSION_KEY_GET][QS_KEY_TOKEN]
            )
            self.executor.plan.context[PLAN_CONTEXT_PENDING_USER] = token.user
            token.delete()
            messages.success(request, _("Successfully verified Email."))
            return self.executor.stage_ok()
        if PLAN_CONTEXT_PENDING_USER not in self.executor.plan.context:
            messages.error(self.request, _("No pending user."))
            return self.executor.stage_invalid()
        # Check if we've already sent the initial e-mail
        if PLAN_CONTEXT_EMAIL_SENT not in self.executor.plan.context:
            self.send_email()
            self.executor.plan.context[PLAN_CONTEXT_EMAIL_SENT] = True
        return super().get(request, *args, **kwargs)

    def form_invalid(self, form: EmailStageSendForm) -> HttpResponse:
        if PLAN_CONTEXT_PENDING_USER not in self.executor.plan.context:
            messages.error(self.request, _("No pending user."))
            return super().form_invalid(form)
        self.send_email()
        # We can't call stage_ok yet, as we're still waiting
        # for the user to click the link in the email
        return super().form_invalid(form)
