from django import forms
from .models import Trip, Country, City

class TripForm(forms.ModelForm):
    """여행 생성/수정 폼"""
    
    # Country 선택 후 → 해당 국가의 City만 보이도록 (JavaScript 필요)
    # 일단은 모든 Country, City를 보여주는 방식으로 구현
    
    class Meta:
        model = Trip
        fields = ['name', 'country', 'city', 'start_date', 'end_date', 'memo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '예: 도쿄 여행'}),
            'country': forms.Select(attrs={'class': 'form-control'}),  # TextInput → Select
            'city': forms.Select(attrs={'class': 'form-control'}),      # TextInput → Select
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'memo': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': '여행 메모'}),
        }
        labels = {
            'name': '여행명',
            'country': '국가',
            'city': '도시',
            'start_date': '시작일',
            'end_date': '종료일',
            'memo': '메모',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError('종료일은 시작일보다 이후여야 합니다.')
        
        return cleaned_data