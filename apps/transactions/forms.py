from django import forms
from .models import Transaction, Receipt

class TransactionForm(forms.ModelForm):
    """거래 생성/수정 폼"""
    receipt = forms.FileField(required=False, label='영수증')
    
    class Meta:
        model = Transaction
        fields = ['account', 'trip', 'category', 'transaction_type', 
                  'amount', 'occurred_at', 'merchant', 'memo']
        widgets = {
            'account': forms.Select(attrs={'class': 'form-control'}),
            'trip': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'occurred_at': forms.DateTimeInput(attrs={
                'class': 'form-control', 
                'type': 'datetime-local'
            }),
            'merchant': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '가맹점명'}),
            'memo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'account': '계좌',
            'trip': '여행',
            'category': '카테고리',
            'transaction_type': '거래 유형',
            'amount': '금액',
            'occurred_at': '거래일시',
            'merchant': '가맹점',
            'memo': '메모',
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['account'].queryset = user.accounts.filter(is_active=True)
            self.fields['trip'].queryset = user.trips.all()
        self.fields['trip'].required = False

class TransactionFilterForm(forms.Form):
    """거래 필터 폼"""
    category = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label='전체 카테고리',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    transaction_type = forms.ChoiceField(
        choices=[('', '전체'), ('income', '입금'), ('expense', '출금')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Category
        self.fields['category'].queryset = Category.objects.all()