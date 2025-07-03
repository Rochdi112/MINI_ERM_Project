from django import forms
from .models import Client, Site

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = '__all__'
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
        }
