from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from core.mixins import UserOwnershipMixin
from .models import Transaction, Receipt
from .forms import TransactionForm, TransactionFilterForm

class TransactionListView(UserOwnershipMixin, ListView):
    """거래 목록 뷰"""
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            'account', 'trip', 'category'
        ).prefetch_related('receipts')
        
        category = self.request.GET.get('category')
        transaction_type = self.request.GET.get('transaction_type')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        trip_id = self.request.GET.get('trip')#추가하였음
        if trip_id:                           #추가하였음
            queryset = queryset.filter(trip_id=trip_id) #추가하였음
        if category:
            queryset = queryset.filter(category_id=category)
        
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        
        if start_date:
            queryset = queryset.filter(occurred_at__date__gte=start_date)
        
        if end_date:
            queryset = queryset.filter(occurred_at__date__lte=end_date)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['filter_form'] = TransactionFilterForm(self.request.GET)
        context['filter_form'] = TransactionFilterForm(self.request.GET, user=self.request.user)
        context['total_amount'] = sum(t.amount for t in context['transactions'])
        return context

class TransactionDetailView(UserOwnershipMixin, DetailView):
    """거래 상세 뷰"""
    model = Transaction
    template_name = 'transactions/transaction_detail.html'
    context_object_name = 'transaction'

class TransactionCreateView(UserOwnershipMixin, CreateView):
    """거래 생성 뷰"""
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transaction_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        
        receipt_file = self.request.FILES.get('receipt')
        if receipt_file:
            Receipt.objects.create(
                transaction=self.object,
                file=receipt_file
            )
        
        messages.success(self.request, '거래가 등록되었습니다.')
        return response

class TransactionUpdateView(UserOwnershipMixin, UpdateView):
    """거래 수정 뷰"""
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transaction_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        receipt_file = self.request.FILES.get('receipt')
        if receipt_file:
            Receipt.objects.create(
                transaction=self.object,
                file=receipt_file
            )
        
        messages.success(self.request, '거래 정보가 수정되었습니다.')
        return super().form_valid(form)

class TransactionDeleteView(UserOwnershipMixin, DeleteView):
    """거래 삭제 뷰"""
    model = Transaction
    template_name = 'transactions/transaction_confirm_delete.html'
    success_url = reverse_lazy('transaction_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, '거래가 삭제되었습니다.')
        return super().delete(request, *args, **kwargs)
