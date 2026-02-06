from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone
from apps.trips.models import Trip, Country
from apps.transactions.models import Transaction, Category # Category 추가
from apps.accounts.models import Profile, Account

class MainViewSimpleTest(TestCase):
    def setUp(self):
        # 1. 기본 관계 데이터 생성
        self.user = User.objects.create_user(username='testuser')
        Profile.objects.create(user=self.user, age_group='20')
        
        country = Country.objects.create(name="Japan")
        account = Account.objects.create(user=self.user, name="Main")
        # 카테고리 데이터 생성
        category = Category.objects.create(name="식비")
        
        self.trip = Trip.objects.create(
            user=self.user, 
            country=country, 
            start_date=timezone.now().date(),
            end_date=timezone.now().date()
        )

        # 2. 지출 데이터 생성 (category 추가)
        common_kwargs = {
            'user': self.user,
            'trip': self.trip,
            'account': account,
            'category': category, # 필수 필드 추가
            'occurred_at': timezone.now(),
        }

        Transaction.objects.create(amount=1000, transaction_type='expense', **common_kwargs)
        Transaction.objects.create(amount=2000, transaction_type='expense', **common_kwargs)
        Transaction.objects.create(amount=5000, transaction_type='income', **common_kwargs)

    def test_total_expense_calculation(self):
        """총 지출액 합계 로직 검증"""
        total_spent_all = Transaction.objects.filter(
            transaction_type='expense'
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        # 예상 결과: 1000 + 2000 = 3000
        self.assertEqual(total_spent_all, 3000)