from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
        # 각 기능을 담당하는 앱들
    path('accounts/', include('apps.accounts.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('trips/', include('apps.trips.urls')),
    path('transactions/', include('apps.transactions.urls')),
    # 루트 주소는 main 앱의 urls.py에서 관리하도록 넘깁니다.
    path('', include('apps.main.urls')), 
]