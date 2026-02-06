from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.trips.models import Country, City, Trip
from apps.accounts.models import Account
from apps.transactions.models import Category, Transaction
from django.utils import timezone
from decimal import Decimal

class DashboardAccessTest(TestCase):
    """테스트 1: 대시보드 접근 권한 테스트"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # 실제 대시보드 URL 경로를 지정합니다.
        self.dashboard_url = '/dashboard/'
    
    def test_dashboard_requires_login(self):
        """로그인 없이 접근 시 로그인 페이지로 리다이렉트"""
        response = self.client.get(self.dashboard_url)
        # 비로그인 시 302 리다이렉트가 발생하는지 확인
        self.assertEqual(response.status_code, 302, "비로그인 시 302 리다이렉트가 필요합니다.")
    
    def test_dashboard_accessible_with_login(self):
        """로그인 후에는 대시보드 정상 접근"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/dashboard.html')


class DashboardCategoryStatsTest(TestCase):
    """테스트 2: 카테고리별 통계 계산 테스트"""
    
    def setUp(self):
        self.client = Client()
        self.dashboard_url = '/dashboard/'
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # 계좌 생성
        self.account = Account.objects.create(
            user=self.user,
            name='신한은행',
            bank_name='신한은행',
            account_number='110-123-456789'
        )
        
        # 국가, 도시 생성
        self.country = Country.objects.create(name="일본")
        self.city = City.objects.create(name="도쿄", country=self.country)
        
        # 여행 생성
        self.trip = Trip.objects.create(
            user=self.user,
            name="도쿄 여행",
            country=self.country,
            city=self.city,
            start_date="2026-03-01"
        )
        
        # 카테고리 생성
        self.category_food = Category.objects.create(name="식비")
        self.category_transport = Category.objects.create(name="교통비")
        
        # 거래 생성 (식비 60%, 교통비 40%)
        Transaction.objects.create(
            user=self.user,
            account=self.account,
            trip=self.trip,
            category=self.category_food,
            transaction_type='expense',
            amount=Decimal('60000'),
            occurred_at=timezone.now()
        )
        Transaction.objects.create(
            user=self.user,
            account=self.account,
            trip=self.trip,
            category=self.category_transport,
            transaction_type='expense',
            amount=Decimal('40000'),
            occurred_at=timezone.now()
        )
    
    def test_category_percentage_calculation(self):
        """카테고리별 퍼센트가 정확하게 계산되는지 확인"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.dashboard_url)
        
        # View에서 데이터를 보내주는지 확인
        self.assertIn('category_stats', response.context, "View의 context에 'category_stats'가 없습니다.")
        category_stats = response.context['category_stats']
        
        # 카테고리 통계가 존재하는지
        self.assertGreater(len(category_stats), 0)
        
        # 퍼센트 합계가 100%인지 확인
        total_percentage = sum(float(stat.get('percentage', 0)) for stat in category_stats)
        self.assertAlmostEqual(total_percentage, 100.0, places=1)
        
        # 식비가 60% 정도인지 확인
        food_stat = next((s for s in category_stats if s.get('category__name') == '식비'), None)
        self.assertIsNotNone(food_stat)
        self.assertAlmostEqual(float(food_stat.get('percentage', 0)), 60.0, places=1)


class DashboardUserIsolationTest(TestCase):
    """테스트 3: 사용자 데이터 격리 테스트"""
    
    def setUp(self):
        self.client = Client()
        self.dashboard_url = '/dashboard/'
        
        # 두 명의 사용자 생성
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        
        # 각 사용자별 계좌 생성
        self.account1 = Account.objects.create(user=self.user1, name='계좌1', bank_name='은1', account_number='111')
        self.account2 = Account.objects.create(user=self.user2, name='계좌2', bank_name='은2', account_number='222')
        
        self.country = Country.objects.create(name="한국")
        self.city = City.objects.create(name="서울", country=self.country)
        
        # 각 사용자별 여행 생성
        self.trip1 = Trip.objects.create(user=self.user1, name="user1의 여행", country=self.country, city=self.city, start_date="2026-03-01")
        self.trip2 = Trip.objects.create(user=self.user2, name="user2의 여행", country=self.country, city=self.city, start_date="2026-03-01")
        
        self.category = Category.objects.create(name="식비")
        
        # 각 사용자별 거래 생성
        Transaction.objects.create(user=self.user1, account=self.account1, trip=self.trip1, category=self.category, 
                                   transaction_type='expense', amount=Decimal('100000'), occurred_at=timezone.now())
        Transaction.objects.create(user=self.user2, account=self.account2, trip=self.trip2, category=self.category, 
                                   transaction_type='expense', amount=Decimal('200000'), occurred_at=timezone.now())
    
    def test_user_only_sees_own_trips(self):
        """사용자는 자신의 여행 통계만 볼 수 있음"""
        self.client.login(username='user1', password='pass123')
        response = self.client.get(self.dashboard_url)
        
        self.assertIn('trip_stats', response.context, "View의 context에 'trip_stats'가 없습니다.")
        trip_stats = response.context['trip_stats']
        
        # 객체 리스트인지 딕셔너리 리스트인지에 따른 처리
        try:
            trip_names = [trip.name for trip in trip_stats]
        except AttributeError:
            trip_names = [trip['name'] for trip in trip_stats]
        
        self.assertIn("user1의 여행", trip_names)
        self.assertNotIn("user2의 여행", trip_names)
    
    def test_user_only_sees_own_expenses(self):
        """사용자는 자신의 지출 통계만 볼 수 있음"""
        self.client.login(username='user1', password='pass123')
        response = self.client.get(self.dashboard_url)
        
        self.assertIn('category_stats', response.context, "View의 context에 'category_stats'가 없습니다.")
        category_stats = response.context['category_stats']
        
        # user1의 지출(10만원)만 집계되어야 함
        food_stat = next((s for s in category_stats if s.get('category__name') == '식비'), None)
        self.assertIsNotNone(food_stat)
        self.assertEqual(Decimal(str(food_stat.get('total'))), Decimal('100000'))