from __future__ import annotations

from django.contrib.auth import get_user_model
from django.test import TestCase

try:
    from apps.accounts.forms import SignUpForm
except Exception:
    SignUpForm = None


User = get_user_model()


class SignUpFormTests(TestCase):
    def test_signup_form_importable(self):
        # 프로젝트에 SignUpForm이 없으면 이 테스트를 삭제하거나 경로를 수정하세요.
        self.assertIsNotNone(SignUpForm)

    def test_email_must_be_unique(self):
        if SignUpForm is None:
            self.skipTest("SignUpForm not available in apps.accounts.forms")

        User.objects.create_user(username="u1", email="dup@example.com", password="pass1234!")
        form = SignUpForm(data={
            "username": "u2",
            "email": "dup@example.com",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
