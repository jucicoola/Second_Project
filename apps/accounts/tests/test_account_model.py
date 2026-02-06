from __future__ import annotations

from django.test import TestCase

from apps.accounts.models import Account
from apps.transactions.tests.utils import make_user


class AccountModelTests(TestCase):
    def test_account_str_not_empty(self):
        u = make_user("u1")
        acc = Account.objects.create(
            user=u,
            name="생활비",
            bank_name="테스트은행",
            account_number="000-000",
            is_active=True,
        )
        self.assertTrue(str(acc))
