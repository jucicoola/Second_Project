from django.db import models
from django.contrib.auth.models import User

class Country(models.Model):
    """국가 모델"""
    name = models.CharField(max_length=100, unique=True, verbose_name='국가명')
    
    class Meta:
        verbose_name = '국가'
        verbose_name_plural = '국가 목록'
    
    def __str__(self):
        return self.name


class City(models.Model):
    """도시 모델"""
    name = models.CharField(max_length=100, verbose_name='도시명')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')
    
    class Meta:
        verbose_name = '도시'
        verbose_name_plural = '도시 목록'
        unique_together = ['name', 'country']
    
    def __str__(self):
        return f"{self.name} ({self.country.name})"


class Trip(models.Model):
    """여행 모델"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips')
    name = models.CharField(max_length=100, verbose_name='여행명')
    
    # CharField → ForeignKey로 변경
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name='국가')
    city = models.ForeignKey(City, on_delete=models.PROTECT, blank=True, null=True, verbose_name='도시')
    
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
        return f"{self.name} ({self.country.name})"
    
    def get_duration_days(self):
        """여행 기간 계산"""
        if self.end_date:
            return (self.end_date - self.start_date).days + 1
        return 1