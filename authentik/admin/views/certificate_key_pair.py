"""authentik CertificateKeyPair administration"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import (
    PermissionRequiredMixin as DjangoPermissionRequiredMixin,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView, UpdateView
from guardian.mixins import PermissionListMixin, PermissionRequiredMixin

from authentik.admin.views.utils import (
    BackSuccessUrlMixin,
    DeleteMessageView,
    SearchListMixin,
    UserPaginateListMixin,
)
from authentik.crypto.forms import CertificateKeyPairForm
from authentik.crypto.models import CertificateKeyPair
from authentik.lib.views import CreateAssignPermView


class CertificateKeyPairListView(
    LoginRequiredMixin,
    PermissionListMixin,
    UserPaginateListMixin,
    SearchListMixin,
    ListView,
):
    """Show list of all keypairs"""

    model = CertificateKeyPair
    permission_required = "authentik_crypto.view_certificatekeypair"
    ordering = "name"
    template_name = "administration/certificatekeypair/list.html"

    search_fields = ["name"]


class CertificateKeyPairCreateView(
    SuccessMessageMixin,
    BackSuccessUrlMixin,
    LoginRequiredMixin,
    DjangoPermissionRequiredMixin,
    CreateAssignPermView,
):
    """Create new CertificateKeyPair"""

    model = CertificateKeyPair
    form_class = CertificateKeyPairForm
    permission_required = "authentik_crypto.add_certificatekeypair"

    template_name = "generic/create.html"
    success_url = reverse_lazy("authentik_admin:certificate_key_pair")
    success_message = _("Successfully created CertificateKeyPair")


class CertificateKeyPairUpdateView(
    SuccessMessageMixin,
    BackSuccessUrlMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    """Update certificatekeypair"""

    model = CertificateKeyPair
    form_class = CertificateKeyPairForm
    permission_required = "authentik_crypto.change_certificatekeypair"

    template_name = "generic/update.html"
    success_url = reverse_lazy("authentik_admin:certificate_key_pair")
    success_message = _("Successfully updated Certificate-Key Pair")


class CertificateKeyPairDeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, DeleteMessageView
):
    """Delete certificatekeypair"""

    model = CertificateKeyPair
    permission_required = "authentik_crypto.delete_certificatekeypair"

    template_name = "generic/delete.html"
    success_url = reverse_lazy("authentik_admin:certificate_key_pair")
    success_message = _("Successfully deleted Certificate-Key Pair")
