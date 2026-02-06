from __future__ import annotations

from decimal import Decimal
from datetime import datetime, timezone

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.transactions.models import Category, Transaction
from .utils import make_user, make_account, make_category, make_tx


class CategoryModelTests(TestCase):
    def test_str_returns_name(self):
        c = make_category(name="교통")
        self.assertEqual(str(c), "교통")

    def test_unique_name(self):
        make_category(name="식비")
        with self.assertRaises(Exception):
            make_category(name="식비")


class TransactionModelTests(TestCase):
    def test_str_contains_type_amount_category(self):
        u = make_user("u1")
        acc = make_account(u)
        cat = make_category("식비")
        tx = make_tx(user=u, account=acc, category=cat, tx_type="expense", amount=Decimal("1234.00"))
        s = str(tx)
        self.assertIn("출금", s)  # get_transaction_type_display()
        self.assertIn("1234.00", s)
        self.assertIn("식비", s)

    def test_amount_min_value_validator(self):
        u = make_user("u1")
        acc = make_account(u)
        cat = make_category("식비")
        tx = Transaction(
            user=u,
            account=acc,
            category=cat,
            transaction_type="expense",
            amount=Decimal("-1.00"),
            occurred_at=datetime(2026, 2, 1, 12, 0, tzinfo=timezone.utc),
        )
        with self.assertRaises(ValidationError):
            tx.full_clean()  # MinValueValidator(0)

    def test_default_ordering_is_desc_occurred_at(self):
        u = make_user("u1")
        acc = make_account(u)
        cat = make_category("식비")

        t1 = make_tx(
            user=u, account=acc, category=cat,
            occurred_at=datetime(2026, 2, 1, 12, 0, tzinfo=timezone.utc),
        )
        t2 = make_tx(
            user=u, account=acc, category=cat,
            occurred_at=datetime(2026, 2, 2, 12, 0, tzinfo=timezone.utc),
            amount=Decimal("2000.00"),
        )

        qs = list(Transaction.objects.all())
        self.assertEqual(qs[0].id, t2.id)
        self.assertEqual(qs[1].id, t1.id)
