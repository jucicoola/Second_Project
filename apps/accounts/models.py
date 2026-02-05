from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    """계좌 모델"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    name = models.CharField(max_length=100, verbose_name='계좌명')
    bank_name = models.CharField(max_length=100, verbose_name='은행명')
    account_number = models.CharField(max_length=50, verbose_name='계좌번호')
    is_active = models.BooleanField(default=True, verbose_name='활성화 상태')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일시')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일시')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = '계좌'
        verbose_name_plural = '계좌 목록'
    
    def __str__(self):
        return f"{self.name} ({self.bank_name})"

class Profile(models.Model):
    """사용자 프로필 - 연령대/성별 정보"""
    
    AGE_CHOICES = [
        ('10s', '10대'),
        ('20s', '20대'),
        ('30s', '30대'),
        ('40s', '40대'),
        ('50s', '50대 이상'),
    ]
    
    GENDER_CHOICES = [
        ('M', '남성'),
        ('F', '여성'),
        ('O', '기타'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age_group = models.CharField(max_length=3, choices=AGE_CHOICES, verbose_name='연령대')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='성별')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = '프로필'
        verbose_name_plural = '프로필 목록'
    
    def __str__(self):
        return f"{self.user.username}의 프로필"