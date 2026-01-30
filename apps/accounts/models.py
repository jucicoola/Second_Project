from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Account(models.Model):
    """계좌 모델"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    name = models.CharField(max_length=100, verbose_name='계좌명')
    bank_name = models.CharField(max_length=100, verbose_name='은행명')
    account_number = models.CharField(max_length=50, verbose_name='계좌번호')
    initial_balance = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        verbose_name='초기잔액'
    )
    is_active = models.BooleanField(default=True, verbose_name='활성화 상태')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일시')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일시')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = '계좌'
        verbose_name_plural = '계좌 목록'
    
    def __str__(self):
        return f"{self.name} ({self.bank_name})"
