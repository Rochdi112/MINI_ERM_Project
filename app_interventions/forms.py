from django import forms
from .models import Intervention, ChecklistItem, Attachment
from django.core.exceptions import ValidationError
import os

class InterventionForm(forms.ModelForm):
    class Meta:
        model = Intervention
        fields = ['client', 'materiel', 'technicien', 'type', 'statut', 'date_cloture', 'description']
        widgets = {
            'materiel': forms.Select(attrs={'class': 'form-select'}),
            'technicien': forms.Select(attrs={'class': 'form-select'}),
            'site': forms.Select(attrs={'class': 'form-select'}),
        }

class ChecklistItemForm(forms.ModelForm):
    class Meta:
        model = ChecklistItem
        fields = ['description', 'completed']

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
        max_size = 5 * 1024 * 1024
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in allowed_extensions:
            raise forms.ValidationError("Extension non autorisée.")
        if file.size > max_size:
            raise forms.ValidationError("Fichier trop volumineux (max 5 Mo).")
        if ext in ['.exe', '.js', '.bat', '.sh']:
            raise forms.ValidationError("Type de fichier interdit.")
        return file
