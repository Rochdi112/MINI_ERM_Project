from django import forms
from .models import Intervention

class InterventionForm(forms.ModelForm):
    class Meta:
        model = Intervention
        fields = ['client', 'materiel', 'technicien', 'type', 'statut', 'date_cloture', 'description']
