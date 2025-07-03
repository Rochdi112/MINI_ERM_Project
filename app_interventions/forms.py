from django import forms
from .models import Intervention, ChecklistItem
from django.core.exceptions import ValidationError
import os

class InterventionForm(forms.ModelForm):
    class Meta:
        model = Intervention
        fields = ['client', 'materiel', 'techniciens', 'site', 'type', 'statut', 'date_cloture', 'description']
        widgets = {
            'materiel': forms.Select(attrs={'class': 'form-select'}),
            'techniciens': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'site': forms.Select(attrs={'class': 'form-select'}),
        }

class ChecklistItemForm(forms.ModelForm):
    class Meta:
        model = ChecklistItem
        fields = ['description', 'completed']
