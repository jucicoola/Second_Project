from django.db import models
from django.contrib.auth.models import User

class Trip(models.Model):
    """여행 모델"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips')
    name = models.CharField(max_length=100, verbose_name='여행명')
    country = models.CharField(max_length=100, verbose_name='국가')
    city = models.CharField(max_length=100, blank=True, verbose_name='도시')
    start_date = models.DateField(verbose_name='시작일')
    end_date = models.DateField(null=True, blank=True, verbose_name='종료일')
    memo = models.TextField(blank=True, verbose_name='메모')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일시')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일시')
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = '여행'
        verbose_name_plural = '여행 목록'
    
    def __str__(self):
        return f"{self.name} ({self.country})"
    
    def get_duration_days(self):
        """여행 기간 계산"""
        if self.end_date:
            return (self.end_date - self.start_date).days + 1
        return 1
