from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from apps.accounts.models import Account
from apps.trips.models import Trip
from core.validators import validate_file_extension, validate_file_size

class Category(models.Model):
    """카테고리 모델"""
    name = models.CharField(max_length=50, unique=True, verbose_name='카테고리명')
    description = models.TextField(blank=True, verbose_name='설명')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일시')
    
    class Meta:
        ordering = ['name']
        verbose_name = '카테고리'
        verbose_name_plural = '카테고리 목록'
    
    def __str__(self):
        return self.name

class Transaction(models.Model):
    """거래 모델"""
    TRANSACTION_TYPE_CHOICES = [
        ('income', '입금'),
        ('expense', '출금'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transaction_set')
    trip = models.ForeignKey(
        Trip, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='transaction_set'
    )
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='transactions')
    transaction_type = models.CharField(
        max_length=10, 
        choices=TRANSACTION_TYPE_CHOICES,
        verbose_name='거래유형'
    )
    amount = models.DecimalField(
        max_digits=15, 
        decimal_places=0,
        validators=[MinValueValidator(0)],
        verbose_name='금액'
    )
    occurred_at = models.DateTimeField(db_index=True, verbose_name='거래일시')
    merchant = models.CharField(max_length=200, blank=True, verbose_name='가맹점')
    memo = models.TextField(blank=True, verbose_name='메모')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일시')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일시')
    
    class Meta:
        ordering = ['-occurred_at']
        indexes = [
            models.Index(fields=['-occurred_at']),
            models.Index(fields=['user', 'occurred_at']),
        ]
        verbose_name = '거래'
        verbose_name_plural = '거래 목록'
    
    def __str__(self):
        return f"{self.get_transaction_type_display()} {self.amount}원 - {self.category}"

class Receipt(models.Model):
    """영수증 모델"""
    transaction = models.ForeignKey(
        Transaction, 
        on_delete=models.CASCADE, 
        related_name='receipts'
    )
    file = models.FileField(
        upload_to='receipts/%Y/%m/%d/',
        validators=[validate_file_extension, validate_file_size],
        verbose_name='영수증 파일'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='업로드일시')
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = '영수증'
        verbose_name_plural = '영수증 목록'
    
    def __str__(self):
        return f"영수증 - {self.transaction}"
