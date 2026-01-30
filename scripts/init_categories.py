#!/usr/bin/env python
"""
초기 카테고리 데이터 생성 스크립트
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.transactions.models import Category

INITIAL_CATEGORIES = [
    {'name': '식비', 'description': '식사, 음료 등'},
    {'name': '교통', 'description': '교통비, 택시, 렌터카 등'},
    {'name': '숙박', 'description': '호텔, 숙소 비용'},
    {'name': '쇼핑', 'description': '쇼핑, 선물 구매'},
    {'name': '관광', 'description': '입장료, 투어 비용'},
    {'name': '기타', 'description': '기타 비용'},
]

def init_categories():
    """초기 카테고리 생성"""
    for cat_data in INITIAL_CATEGORIES:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        if created:
            print(f"✓ 카테고리 생성: {category.name}")
        else:
            print(f"- 카테고리 존재: {category.name}")

if __name__ == '__main__':
    print("카테고리 초기화 시작...")
    init_categories()
    print("카테고리 초기화 완료!")
