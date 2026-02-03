from django.shortcuts import render
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum, Q
from core.mixins import UserOwnershipMixin
from .models import Trip
from .forms import TripForm

class TripListView(UserOwnershipMixin, ListView):
    """여행 목록 뷰: 로그인한 사용자의 여행만 표시"""
    model = Trip
    template_name = 'trips/trip_list.html'
    context_object_name = 'trips'
    paginate_by = 20

class TripDetailView(UserOwnershipMixin, DetailView):
    """
    여행 상세 뷰: 
    메인 화면에서 클릭 시 UserOwnershipMixin에 의해 로그인 여부를 확인하고, 
    로그인되지 않았다면 로그인 페이지로 리다이렉트합니다.
    """
    model = Trip
    template_name = 'trips/trip_detail.html'
    context_object_name = 'trip'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip = self.object
        
        # 해당 여행에 연결된 모든 거래(지출/수입) 내역을 가져옵니다.
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
        # 현재 로그인한 사용자를 여행 정보의 주인으로 저장
        form.instance.user = self.request.user
        messages.success(self.request, '새로운 여행이 등록되었습니다.')
        return super().form_valid(form)

class TripUpdateView(UserOwnershipMixin, UpdateView):
    """여행 정보 수정 뷰"""
    model = Trip
    form_class = TripForm
    template_name = 'trips/trip_form.html'
    success_url = reverse_lazy('trip_list')
    
    def form_valid(self, form):
        messages.success(self.request, '여행 정보가 성공적으로 수정되었습니다.')
        return super().form_valid(form)

class TripDeleteView(UserOwnershipMixin, DeleteView):
    """여행 삭제 뷰"""
    model = Trip
    template_name = 'trips/trip_confirm_delete.html'
    success_url = reverse_lazy('trip_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, '여행 정보가 삭제되었습니다.')
        return super().delete(request, *args, **kwargs)