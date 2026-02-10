from django.views.generic import TemplateView
from django.contrib.auth.models import User
from apps.trips.models import Trip
from apps.transactions.models import Transaction
from apps.accounts.models import Profile
from django.db.models import Sum, Count

class MainView(TemplateView):
    template_name = 'main/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 1. 최근 여행지 3곳 (각 여행별 지출 총액 포함)
        recent_trips = Trip.objects.all().order_by('-created_at')[:3]
        
        for trip in recent_trips:
            # 각 여행 객체에 'total_spent'라는 속성을 실시간으로 계산해서 붙여줍니다.
            trip.total_spent = Transaction.objects.filter(
                trip=trip, 
                transaction_type='expense'
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
        context['recent_trips'] = recent_trips

        # 2. 서비스 통계 요약 데이터
        # 총 사용자 수
        context['total_users'] = User.objects.count()
        
        # 전체 여행지 개수
        context['total_trips'] = Trip.objects.count()
        
        # 누적 지출 금액 (전체 거래 중 '출금'만 합산)
        total_spent_all = Transaction.objects.filter(
            transaction_type='expense'
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        context['total_spent_all'] = total_spent_all
        
        # 3. 국가별 여행 지출 TOP 3 (그래프용 데이터)
        top_expenses = (
            Transaction.objects.filter(transaction_type='expense', trip__isnull=False)
            .values('trip__country__name')  
            .annotate(total=Sum('amount'))
            .order_by('-total')[:3]
        )
        
        context['labels'] = [item['trip__country__name'] for item in top_expenses]
        context['data'] = [float(item['total']) for item in top_expenses]

        # 4. 모든 연령대별 인기 여행지 TOP 3
        age_group_data = []
        
        for age_code, age_label in Profile.AGE_CHOICES:
            # 각 연령대별로 인기 여행지 TOP 3 조회
            destinations = (
                Trip.objects
                .filter(user__profile__age_group=age_code)
                .values('country__name', 'city__name')
                .annotate(visit_count=Count('id'))
                .order_by('-visit_count')
                [:3]
            )
            
            age_group_data.append({
                'age_label': age_label,  # '10대', '20대' 등
                'destinations': list(destinations)  # TOP 3 여행지 리스트
            })
        
        context['age_group_data'] = age_group_data
        
        return context 