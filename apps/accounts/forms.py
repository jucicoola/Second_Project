from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Account, Profile

class SignUpForm(UserCreationForm):
    """회원가입 폼"""
    email = forms.EmailField(  # 이메일 자동검사
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '이메일'})
    ) # 입력창 태그 안에 들어가는 옵션들
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

    age_group = forms.ChoiceField(
        choices=Profile.AGE_CHOICES,
        label='연령대',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    gender = forms.ChoiceField(
        choices=Profile.GENDER_CHOICES,
        label='성별',
        widget=forms.RadioSelect()  # 라디오 버튼
    )
    
    # label -> 한국어로 바꾸고 싶을 때, 기본 이름 이상해서 변경하고 싶을 때 사용

    class Meta:
        model = User # 장고 기본 User 테이블, 회원가입하면 User 테이블에 저장 
        fields = ('username', 'email', 'password1', 'password2') # 화면에 보여주고 저장할 필드 목록
    
    def clean_email(self): # clean_필드명: 해당 필드 검증 규칙
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('이미 사용 중인 이메일입니다.')
        return email

class AccountForm(forms.ModelForm): # ModelForm = 모델을 기반으로 자동 생성되는 DB 연결 폼
    """계좌 생성/수정 폼"""
    class Meta:
        model = Account
        fields = ['name', 'bank_name', 'account_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '예: 신한은행 주계좌'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '예: 신한은행'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '예: 110-123-456789'}),
        }
        labels = {
            'name': '계좌명',
            'bank_name': '은행명',
            'account_number': '계좌번호',
        }
