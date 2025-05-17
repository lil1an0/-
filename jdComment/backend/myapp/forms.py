from django import forms
from .models import SalesRecord

class SalesRecordForm(forms.ModelForm):
    class Meta:
        model = SalesRecord
        fields = '__all__'  # 包括所有字段
        widgets = {
            'sales_date': forms.DateInput(attrs={'type': 'date'}),
        }
