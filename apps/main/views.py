from django.views.generic import TemplateView
from django.contrib.auth.models import User
from apps.trips.models import Trip
from apps.transactions.models import Transaction
from django.db.models import Sum

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
            .values('trip__country')
            .annotate(total=Sum('amount'))
            .order_by('-total')[:3]
        )
        
        context['labels'] = [item['trip__country'] for item in top_expenses]
        context['data'] = [float(item['total']) for item in top_expenses]
        
        return context