from django.contrib import admin
from .models import Category, Transaction, Receipt

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['occurred_at', 'transaction_type', 'amount', 'category', 
                    'merchant', 'user', 'account']
    list_filter = ['transaction_type', 'category', 'occurred_at']
    search_fields = ['category__name', 'merchant', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'occurred_at'

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ['transaction', 'file', 'uploaded_at']
    readonly_fields = ['uploaded_at']
