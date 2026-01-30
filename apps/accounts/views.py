from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from core.mixins import UserOwnershipMixin
from .models import Account
from .forms import SignUpForm, AccountForm

class SignUpView(CreateView):
    """회원가입 뷰"""
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, '회원가입이 완료되었습니다.')
        return response

class LoginView(DjangoLoginView):
    """로그인 뷰"""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        messages.success(self.request, f'{form.get_user().username}님, 환영합니다!')
        return super().form_valid(form)

def logout_view(request):
    """로그아웃 뷰"""
    logout(request)
    messages.info(request, '로그아웃되었습니다.')
    return redirect('login')

class AccountListView(UserOwnershipMixin, ListView):
    """계좌 목록 뷰"""
    model = Account
    template_name = 'accounts/account_list.html'
    context_object_name = 'accounts'
    
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class AccountDetailView(UserOwnershipMixin, DetailView):
    """계좌 상세 뷰"""
    model = Account
    template_name = 'accounts/account_detail.html'
    context_object_name = 'account'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transactions'] = self.object.transaction_set.select_related(
            'category', 'trip'
        ).order_by('-occurred_at')[:20]
        return context

class AccountCreateView(UserOwnershipMixin, CreateView):
    """계좌 생성 뷰"""
    model = Account
    form_class = AccountForm
    template_name = 'accounts/account_form.html'
    success_url = reverse_lazy('account_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, '계좌가 등록되었습니다.')
        return super().form_valid(form)

class AccountUpdateView(UserOwnershipMixin, UpdateView):
    """계좌 수정 뷰"""
    model = Account
    form_class = AccountForm
    template_name = 'accounts/account_form.html'
    success_url = reverse_lazy('account_list')
    
    def form_valid(self, form):
        messages.success(self.request, '계좌 정보가 수정되었습니다.')
        return super().form_valid(form)

class AccountDeleteView(UserOwnershipMixin, DeleteView):
    """계좌 삭제 뷰"""
    model = Account
    template_name = 'accounts/account_confirm_delete.html'
    success_url = reverse_lazy('account_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, '계좌가 삭제되었습니다.')
        return super().delete(request, *args, **kwargs)
