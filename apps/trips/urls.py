from django.urls import path
from . import views

urlpatterns = [
    path('', views.TripListView.as_view(), name='trip_list'),
    path('create/', views.TripCreateView.as_view(), name='trip_create'),
    path('<int:pk>/', views.TripDetailView.as_view(), name='trip_detail'),
    path('<int:pk>/edit/', views.TripUpdateView.as_view(), name='trip_update'),
    path('<int:pk>/delete/', views.TripDeleteView.as_view(), name='trip_delete'),
]
