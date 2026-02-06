from django import forms
from django.db.models import Case, When, Value, IntegerField
from .models import Transaction, Receipt, Category
from apps.trips.models import Trip #추가함

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
        
        # 카테고리 순서: 이름순 정렬, 단 '기타'는 맨 마지막
        self.fields['category'].queryset = Category.objects.annotate(
            custom_order=Case(
                When(name='기타', then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            )
        ).order_by('custom_order', 'name')

class TransactionFilterForm(forms.Form):
    """거래 필터 폼"""
    trip = forms.ModelChoiceField(    # 추가함
        queryset=Trip.objects.none(), # 추가함
        required=False,                # 추가함
        empty_label='전체 여행',          # 추가함
        widget=forms.Select(attrs={'class': 'form-control'}) # 추가함
    ) # 추가함
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
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        # 중요: 현재 로그인한 유저의 여행만 선택지에 노출
        if user and not user.is_superuser:
            self.fields['trip'].queryset = Trip.objects.filter(user=user)
        else:
            self.fields['trip'].queryset = Trip.objects.all()
        
        # 카테고리 정렬 로직 (기존 유지)
        self.fields['category'].queryset = Category.objects.annotate(
            custom_order=Case(When(name='기타', then=Value(1)), default=Value(0), output_field=IntegerField())
        ).order_by('custom_order', 'name')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        
    #     self.fields['category'].queryset = Category.objects.annotate(
    #         custom_order=Case(
    #             When(name='기타', then=Value(1)),
    #             default=Value(0),
    #             output_field=IntegerField()
    #         )
    #     ).order_by('custom_order', 'name')
