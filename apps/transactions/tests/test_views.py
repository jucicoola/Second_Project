from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from apps.transactions.models import Receipt, Transaction
from .utils import make_user, make_account, make_trip, make_category, make_tx


class TransactionViewTests(TestCase):
    def setUp(self):
        self.u1 = make_user("u1", password="pass1234!")
        self.u2 = make_user("u2", password="pass1234!")
        self.a1 = make_account(self.u1)
        self.a2 = make_account(self.u2)
        self.trip1 = make_trip(self.u1)
        self.cat_food = make_category("식비")
        self.cat_misc = make_category("기타")

        self.t1 = make_tx(
            user=self.u1, account=self.a1, category=self.cat_food,
            amount=Decimal("1000.00"),
            occurred_at=datetime(2026, 2, 1, 12, 0, tzinfo=timezone.utc),
            trip=self.trip1,
        )
        self.t2 = make_tx(
            user=self.u2, account=self.a2, category=self.cat_misc,
            amount=Decimal("2000.00"),
            occurred_at=datetime(2026, 2, 2, 12, 0, tzinfo=timezone.utc),
        )

    def test_list_requires_login(self):
        resp = self.client.get(reverse("transaction_list"))
        self.assertEqual(resp.status_code, 302)  # redirect to login

    def test_list_shows_only_own_transactions(self):
        self.client.login(username="u1", password="pass1234!")
        resp = self.client.get(reverse("transaction_list"))
        self.assertEqual(resp.status_code, 200)
        txs = list(resp.context["transactions"])
        self.assertIn(self.t1, txs)
        self.assertNotIn(self.t2, txs)

    def test_list_filter_by_trip(self):
        self.client.login(username="u1", password="pass1234!")
        resp = self.client.get(reverse("transaction_list"), {"trip": self.trip1.id})
        self.assertEqual(resp.status_code, 200)
        txs = list(resp.context["transactions"])
        self.assertEqual(txs, [self.t1])

    def test_detail_forbidden_for_other_users_transaction(self):
        self.client.login(username="u1", password="pass1234!")
        resp = self.client.get(reverse("transaction_detail", kwargs={"pk": self.t2.pk}))
        self.assertIn(resp.status_code, (403, 404))

    def test_create_creates_transaction_and_receipt(self):
        self.client.login(username="u1", password="pass1234!")
        url = reverse("transaction_create")
        file = SimpleUploadedFile("receipt.jpg", b"fakejpgcontent", content_type="image/jpeg")

        payload = {
            "account": self.a1.id,
            "trip": self.trip1.id,
            "category": self.cat_food.id,
            "transaction_type": "expense",
            "amount": "3000.00",
            "occurred_at": "2026-02-03T10:30",
            "merchant": "테스트",
            "memo": "메모",
            "receipt": file,
        }
        resp = self.client.post(url, payload)
        self.assertEqual(resp.status_code, 302)

        tx = Transaction.objects.get(amount=Decimal("3000.00"))
        self.assertEqual(tx.user_id, self.u1.id)
        self.assertTrue(Receipt.objects.filter(transaction=tx).exists())

    def test_update_creates_additional_receipt_when_uploaded(self):
        self.client.login(username="u1", password="pass1234!")
        url = reverse("transaction_update", kwargs={"pk": self.t1.pk})
        file = SimpleUploadedFile("receipt.jpg", b"fakejpgcontent", content_type="image/jpeg")

        payload = {
            "account": self.a1.id,
            "trip": self.trip1.id,
            "category": self.cat_food.id,
            "transaction_type": "expense",
            "amount": "1000.00",
            "occurred_at": "2026-02-01T12:00",
            "merchant": "테스트가맹점",
            "memo": "",
            "receipt": file,
        }
        before = Receipt.objects.filter(transaction=self.t1).count()
        resp = self.client.post(url, payload)
        self.assertEqual(resp.status_code, 302)
        after = Receipt.objects.filter(transaction=self.t1).count()
        self.assertEqual(after, before + 1)

    def test_delete_deletes_transaction(self):
        self.client.login(username="u1", password="pass1234!")
        url = reverse("transaction_delete", kwargs={"pk": self.t1.pk})
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Transaction.objects.filter(pk=self.t1.pk).exists())
