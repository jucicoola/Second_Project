from django.contrib import admin
from .models import Trip

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'city', 'start_date', 'end_date', 'user', 'created_at']
    list_filter = ['country', 'start_date']
    search_fields = ['name', 'country__name', 'city', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
