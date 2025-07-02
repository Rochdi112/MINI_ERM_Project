from django import forms
from .models import Rapport

class RapportForm(forms.ModelForm):
    class Meta:
        model = Rapport
        fields = ['intervention', 'contenu']
