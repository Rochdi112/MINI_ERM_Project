from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Materiel
from .forms import MaterielForm
from core.models import ProfilUtilisateur

class MaterielListView(LoginRequiredMixin, ListView):
    model = Materiel
    template_name = 'app_materiels/materiel_list.html'
    context_object_name = 'materiels'

    def get_queryset(self):
        user_profile = getattr(self.request.user, 'profilutilisateur', None)
        qs = super().get_queryset()
        # Exemple de filtrage par rôle (à adapter selon la logique métier)
        if user_profile and user_profile.role == 'technicien':
            return qs.none()
        return qs

class MaterielCreateView(LoginRequiredMixin, CreateView):
    model = Materiel
    form_class = MaterielForm
    template_name = 'app_materiels/materiel_form.html'
    success_url = reverse_lazy('app_materiels:materiel_list')

    def form_valid(self, form):
        messages.success(self.request, "Matériel créé avec succès.")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, "Erreur lors de la création du matériel.")
        return super().form_invalid(form)

class MaterielUpdateView(LoginRequiredMixin, UpdateView):
    model = Materiel
    form_class = MaterielForm
    template_name = 'app_materiels/materiel_form.html'
    success_url = reverse_lazy('app_materiels:materiel_list')

    def form_valid(self, form):
        messages.success(self.request, "Matériel modifié avec succès.")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, "Erreur lors de la modification du matériel.")
        return super().form_invalid(form)

class MaterielDeleteView(LoginRequiredMixin, DeleteView):
    model = Materiel
    template_name = 'app_materiels/materiel_confirm_delete.html'
    success_url = reverse_lazy('app_materiels:materiel_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Matériel supprimé avec succès.")
        return super().delete(request, *args, **kwargs)
