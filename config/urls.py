from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve  # 추가
from django.urls import re_path       # 추가

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.main.urls')), 
    path('accounts/', include('apps.accounts.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('trips/', include('apps.trips.urls')),
    path('transactions/', include('apps.transactions.urls')),
]

# 운영 환경(DEBUG=False)에서도 미디어 파일을 서빙하기 위한 설정
if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
else:
    # 개발 환경일 때
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)