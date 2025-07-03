from django import forms
from .models import Materiel

class MaterielForm(forms.ModelForm):
    class Meta:
        model = Materiel
        fields = '__all__'
        widgets = {
            'site': forms.Select(attrs={'class': 'form-select'}),
        }
