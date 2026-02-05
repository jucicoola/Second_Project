from django.urls import path
from . import views

# 이 줄이 반드시 있어야 'trips:trip_detail' 형식을 사용할 수 있습니다.
# app_name = 'trips' 

urlpatterns = [
    path('', views.TripListView.as_view(), name='trip_list'),
    path('create/', views.TripCreateView.as_view(), name='trip_create'),
    path('<int:pk>/', views.TripDetailView.as_view(), name='trip_detail'),
    path('<int:pk>/edit/', views.TripUpdateView.as_view(), name='trip_update'),
    path('<int:pk>/delete/', views.TripDeleteView.as_view(), name='trip_delete'),
    path('api/cities/<int:country_id>/', views.get_cities_by_country, name='get_cities_by_country'),
]