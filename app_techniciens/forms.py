from django import forms
from .models import Technicien

class TechnicienForm(forms.ModelForm):
    class Meta:
        model = Technicien
        fields = '__all__'
