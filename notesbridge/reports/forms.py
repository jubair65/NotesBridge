from django import forms
from .models import Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason','details']

        widgets = {
            'reason': forms.Select(attrs={
                'class': 'w-full p-2 border rounded'
            }),
            'details': forms.Textarea(attrs={
                'class': 'w-full p-3 border rounded resize-y',
                'rows': 5,
                'placeholder': 'Add more details (optional)...'
            }),
        }
