from django.contrib import admin
from .models import Account
from core.utils import mask_account_number

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'bank_name', 'masked_account_number', 'user', 'is_active', 'created_at']
    list_filter = ['is_active', 'bank_name', 'created_at']
    search_fields = ['name', 'bank_name', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    
    def masked_account_number(self, obj):
        return mask_account_number(obj.account_number)
    masked_account_number.short_description = '계좌번호'
