from django.views.generic import TemplateView # 데이터 담아서 템플릿에 전달
from django.contrib.auth.mixins import LoginRequiredMixin # 로그인 해야 접속 가능
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth # 날짜를 월 단위로 자르는 함수
from datetime import datetime, timedelta # 파이썬 날짜 계산
from apps.transactions.models import Transaction
from apps.trips.models import Trip

class DashboardView(LoginRequiredMixin, TemplateView):
    """대시보드 뷰"""
    template_name = 'dashboard/dashboard.html'
    
    def get_context_data(self, **kwargs): # 템플릿에 전달할 데이터 묶음
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        context['monthly_stats'] = self.get_monthly_stats(user)
        context['category_stats'] = self.get_category_stats(user)
        context['trip_stats'] = self.get_trip_stats(user)
        context['current_month_summary'] = self.get_current_month_summary(user)
        
        return context
    
    def get_monthly_stats(self, user):
        """월별 지출 통계"""
        six_months_ago = datetime.now() - timedelta(days=180)
        
        monthly_data = Transaction.objects.filter(
            user=user,
            transaction_type='expense',
            occurred_at__gte=six_months_ago
        ).annotate(
            month=TruncMonth('occurred_at')
        ).values('month').annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('month')
        
        return list(monthly_data)
    # 그룹 기준 -> 그룹 -> 그룹 계산
# values: 카테고리 기준 그룹 annotate: 그룹별 계산

    def get_category_stats(self, user):
        """카테고리별 지출 통계"""
        category_data = Transaction.objects.filter(
            user=user,
            transaction_type='expense'
        ).values(
            'category__name'
        ).annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')[:10]
        
        total_expense = sum(item['total'] for item in category_data)
        
        for item in category_data:
            if total_expense > 0:
                item['percentage'] = (item['total'] / total_expense) * 100
            else:
                item['percentage'] = 0
        # percentage 새 필드 
        return list(category_data) # QuerySet -> 리스트로 변환
    
    def get_trip_stats(self, user): # 화면 확인
        """여행별 지출 통계"""
        trips = Trip.objects.filter(user=user).annotate(
            total_expense=Sum(
                'transaction_set__amount',
                filter=models.Q(transaction_set__transaction_type='expense')
            ) # sum() 안에 조건을 넣으려면 Q 객체 형태로만 가능 일반 filter 못씀 (from django.db.models import Q 필요)
        ).order_by('-start_date')[:5]
        
        return trips
    
    def get_current_month_summary(self, user):
        """이번 달 요약"""
        now = datetime.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        transactions = Transaction.objects.filter(
            user=user,
            occurred_at__gte=start_of_month
        )
        
        total_income = transactions.filter(
            transaction_type='income'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        total_expense = transactions.filter(
            transaction_type='expense'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        return {
            'total_income': total_income,
            'total_expense': total_expense,
            'net_amount': total_income - total_expense,
            'transaction_count': transactions.count()
        }

from django.db import models
