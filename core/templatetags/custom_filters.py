from django import template
from core.utils import mask_account_number

register = template.Library()

@register.filter
def mask_account(value):
    """계좌번호 마스킹 필터"""
    return mask_account_number(value)

@register.filter
def currency(value):
    """통화 포맷팅: 1000000 -> 1,000,000원"""
    try:
        return f"{int(value):,}원"
    except (ValueError, TypeError):
        return value
