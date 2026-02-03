from django.urls import path
from .views import MainView  # 여기서 MainView를 가져옵니다.

# app_name = 'main'

urlpatterns = [
    path('', MainView.as_view(), name='main'),
]