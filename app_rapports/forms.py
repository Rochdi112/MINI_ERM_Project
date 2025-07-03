from django import forms
from .models import Rapport

class RapportForm(forms.ModelForm):
    class Meta:
        model = Rapport
        fields = '__all__'
        widgets = {
            'intervention': forms.Select(attrs={'class': 'form-select'}),
        }
