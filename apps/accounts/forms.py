from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Account

class SignUpForm(UserCreationForm):
    """회원가입 폼"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '이메일'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '이름'})
    )
    password1 = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '비밀번호'})
    )
    password2 = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '비밀번호 확인'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('이미 사용 중인 이메일입니다.')
        return email

class AccountForm(forms.ModelForm):
    """계좌 생성/수정 폼"""
    class Meta:
        model = Account
        fields = ['name', 'bank_name', 'account_number', 'initial_balance']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '예: 신한은행 주계좌'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '예: 신한은행'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '예: 110-123-456789'}),
            'initial_balance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0', 'step': '0.01'}),
        }
        labels = {
            'name': '계좌명',
            'bank_name': '은행명',
            'account_number': '계좌번호',
            'initial_balance': '초기잔액',
        }
