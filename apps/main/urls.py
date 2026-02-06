# from django.urls import path
# from .views import MainView  # 여기서 MainView를 가져옵니다.

# app_name = 'main'
#원안
# urlpatterns = [
#     path('', MainView.as_view(), name='main'),
# ]
#1차 수정
# urlpatterns = [
#     path("", MainView.as_view(), name="index"),  # ✅ 여기만 변경
# ]
from django.urls import path
from django.views.generic import RedirectView
from .views import MainView

urlpatterns = [
    path("", MainView.as_view(), name="index"),  # 루트
    path("main/", RedirectView.as_view(pattern_name="index", permanent=False), name="main"),
]