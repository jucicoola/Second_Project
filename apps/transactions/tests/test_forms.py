from __future__ import annotations

from django.test import TestCase

from apps.transactions.forms import TransactionForm, TransactionFilterForm
from .utils import make_user, make_account, make_trip, make_category


class TransactionFormTests(TestCase):
    def test_account_queryset_is_limited_to_active_accounts(self):
        u = make_user("u1")
        a1 = make_account(u, name="A1", is_active=True)
        a2 = make_account(u, name="A2", is_active=False)

        form = TransactionForm(user=u)
        qs = list(form.fields["account"].queryset)
        self.assertIn(a1, qs)
        self.assertNotIn(a2, qs)

    def test_trip_is_optional(self):
        u = make_user("u1")
        make_account(u)
        make_category("식비")
        form = TransactionForm(user=u)
        self.assertFalse(form.fields["trip"].required)

    def test_category_ordering_places_others_before_gita(self):
        make_category("기타")
        make_category("교통")
        make_category("식비")

        form = TransactionForm()
        names = [c.name for c in form.fields["category"].queryset]
        self.assertEqual(names[-1], "기타")

    def test_transaction_filter_form_trip_queryset_is_user_limited_for_normal_user(self):
        u1 = make_user("u1")
        u2 = make_user("u2")
        t1 = make_trip(u1, name="U1 Trip")
        t2 = make_trip(u2, name="U2 Trip")

        f = TransactionFilterForm(user=u1)
        qs = list(f.fields["trip"].queryset)
        self.assertIn(t1, qs)
        self.assertNotIn(t2, qs)

    def test_transaction_filter_form_trip_queryset_all_for_superuser(self):
        su = make_user("admin")
        su.is_superuser = True
        su.is_staff = True
        su.save()

        u = make_user("u1")
        t1 = make_trip(u, name="U1 Trip")

        f = TransactionFilterForm(user=su)
        self.assertIn(t1, list(f.fields["trip"].queryset))
