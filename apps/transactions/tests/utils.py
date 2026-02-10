from __future__ import annotations
from datetime import date, timedelta
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional

from django.contrib.auth import get_user_model

from apps.accounts.models import Account
from apps.trips.models import Trip
from apps.transactions.models import Category, Transaction
from apps.trips.models import Trip, Country, City

User = get_user_model()


def make_user(username: str, password: str = "pass1234!", email: Optional[str] = None):
    if email is None:
        email = f"{username}@example.com"
    return User.objects.create_user(username=username, email=email, password=password)


def make_account(user, name="기본계좌", bank_name="테스트은행", account_number="000-000", is_active=True):
    return Account.objects.create(
        user=user,
        name=name,
        bank_name=bank_name,
        account_number=account_number,
        is_active=is_active,
    )

def make_country(name="Korea"):
    obj, _ = Country.objects.get_or_create(name=name)
    return obj

def make_city(country, name="Seoul"):
    obj, _ = City.objects.get_or_create(country=country, name=name)
    return obj

def make_trip(user, name="Trip1", start_date=None, end_date=None, country=None, city=None, **kwargs):
    if start_date is None:
        start_date = date.today()
    if end_date is None:
        end_date = start_date + timedelta(days=1)

    if country is None:
        country = make_country()
    if city is None:
        city = make_city(country)

    return Trip.objects.create(
        user=user,
        name=name,
        start_date=start_date,
        end_date=end_date,
        country=country, 
        city=city,        
        **kwargs,
    )


def make_category(name="식비", description=""):
    return Category.objects.create(name=name, description=description)


def make_tx(
    *,
    user,
    account,
    category,
    tx_type="expense",
    amount=Decimal("1000"),
    occurred_at: Optional[datetime] = None,
    trip=None,
):
    if occurred_at is None:
        occurred_at = datetime(2026, 2, 1, 12, 0, tzinfo=timezone.utc)
    return Transaction.objects.create(
        user=user,
        account=account,
        trip=trip,
        category=category,
        transaction_type=tx_type,
        amount=amount,
        occurred_at=occurred_at,
        merchant="테스트가맹점",
        memo="",
    )
