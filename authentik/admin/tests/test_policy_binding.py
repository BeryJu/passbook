"""admin tests"""
from uuid import uuid4

from django import forms
from django.test import TestCase
from django.test.client import RequestFactory

from authentik.admin.views.policies_bindings import PolicyBindingCreateView
from authentik.core.models import Application
from authentik.policies.forms import PolicyBindingForm


class TestPolicyBindingView(TestCase):
    """Generic admin tests"""

    def setUp(self):
        self.factory = RequestFactory()

    def test_without_get_param(self):
        """Test PolicyBindingCreateView without get params"""
        request = self.factory.get("/")
        view = PolicyBindingCreateView(request=request)
        self.assertEqual(view.get_initial(), {})

    def test_with_params_invalid(self):
        """Test PolicyBindingCreateView with invalid get params"""
        request = self.factory.get("/", {"target": uuid4()})
        view = PolicyBindingCreateView(request=request)
        self.assertEqual(view.get_initial(), {})

    def test_with_params(self):
        """Test PolicyBindingCreateView with get params"""
        target = Application.objects.create(name="test")
        request = self.factory.get("/", {"target": target.pk.hex})
        view = PolicyBindingCreateView(request=request)
        self.assertEqual(view.get_initial(), {"target": target, "order": 0})

        self.assertTrue(
            isinstance(
                PolicyBindingForm(initial={"target": "foo"}).fields["target"].widget,
                forms.HiddenInput,
            )
        )
