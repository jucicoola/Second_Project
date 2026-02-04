from django.shortcuts import render
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum, Q
from core.mixins import UserOwnershipMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Trip
from .forms import TripForm

class TripListView(UserOwnershipMixin, ListView):
    """여행 목록 뷰: 로그인한 사용자의 여행만 표시"""
    model = Trip
    template_name = 'trips/trip_list.html'
    context_object_name = 'trips'
    paginate_by = 20

    def get_queryset(self):
        # Admin(Superuser)인 경우 모든 여행 목록을 볼 수 있도록 허용
        if self.request.user.is_superuser:
            return Trip.objects.all()
        # 일반 사용자는 본인 데이터만 (UserOwnershipMixin의 기본 동작 보완)
        return super().get_queryset()

class TripDetailView(UserOwnershipMixin, DetailView):
    """
    여행 상세 뷰: 
    로그인 시 본인 데이터가 아니면 404가 발생하던 문제를 
    superuser(admin) 예외 처리를 통해 해결했습니다.
    """
    model = Trip
    template_name = 'trips/trip_detail.html'
    context_object_name = 'trip'
    
    def get_queryset(self):
        # 데이터 소유권 체크 시, Admin은 모든 데이터에 접근 가능하게 수정
        if self.request.user.is_superuser:
            return Trip.objects.all()
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip = self.object
        
        # 해당 여행에 연결된 모든 거래(지출/수입) 내역
        transactions = trip.transaction_set.select_related('account', 'category')
        
        # 지출 합계 계산
        total_expense = transactions.filter(
            transaction_type='expense'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # 수입 합계 계산
        total_income = transactions.filter(
            transaction_type='income'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        context['transactions'] = transactions.order_by('-occurred_at')[:20]
        context['total_expense'] = total_expense
        context['total_income'] = total_income
        context['net_amount'] = total_income - total_expense
        
        return context

class TripCreateView(UserOwnershipMixin, CreateView):
    """여행 등록 뷰"""
    model = Trip
    form_class = TripForm
    template_name = 'trips/trip_form.html'
    success_url = reverse_lazy('trip_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, '새로운 여행이 등록되었습니다.')
        return super().form_valid(form)

class TripUpdateView(UserOwnershipMixin, UpdateView):
    """여행 정보 수정 뷰"""
    model = Trip
    form_class = TripForm
    template_name = 'trips/trip_form.html'
    success_url = reverse_lazy('trip_list')
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Trip.objects.all()
        return super().get_queryset()
    
    def form_valid(self, form):
        messages.success(self.request, '여행 정보가 성공적으로 수정되었습니다.')
        return super().form_valid(form)

class TripDeleteView(UserOwnershipMixin, DeleteView):
    """여행 삭제 뷰"""
    model = Trip
    template_name = 'trips/trip_confirm_delete.html'
    success_url = reverse_lazy('trip_list')
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Trip.objects.all()
        return super().get_queryset()
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, '여행 정보가 삭제되었습니다.')
        return super().delete(request, *args, **kwargs)