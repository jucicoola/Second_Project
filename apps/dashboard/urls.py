# apps/dashboard/urls.py
from django.urls import path
from . import views

# 이 한 줄이 있어야 템플릿에서 'dashboard:'를 사용할 수 있습니다!
# app_name = 'dashboard' 

urlpatterns = [
    path('', views.DashboardView.as_view(), name='index'),
]