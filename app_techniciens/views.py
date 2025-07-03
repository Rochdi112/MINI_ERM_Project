from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Technicien
from .forms import TechnicienForm
from core.models import ProfilUtilisateur

class TechnicienListView(LoginRequiredMixin, ListView):
    model = Technicien
    template_name = 'app_techniciens/technicien_list.html'
    context_object_name = 'techniciens'

    def get_queryset(self):
        user_profile = getattr(self.request.user, 'profilutilisateur', None)
        qs = super().get_queryset()
        # Exemple de filtrage par rôle (à adapter selon la logique métier)
        if user_profile and user_profile.role == 'client':
            return qs.none()
        return qs

class TechnicienCreateView(LoginRequiredMixin, CreateView):
    model = Technicien
    form_class = TechnicienForm
    template_name = 'app_techniciens/technicien_form.html'
    success_url = reverse_lazy('app_techniciens:technicien_list')

    def form_valid(self, form):
        messages.success(self.request, "Technicien créé avec succès.")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, "Erreur lors de la création du technicien.")
        return super().form_invalid(form)

class TechnicienUpdateView(LoginRequiredMixin, UpdateView):
    model = Technicien
    form_class = TechnicienForm
    template_name = 'app_techniciens/technicien_form.html'
    success_url = reverse_lazy('app_techniciens:technicien_list')

    def form_valid(self, form):
        messages.success(self.request, "Technicien modifié avec succès.")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, "Erreur lors de la modification du technicien.")
        return super().form_invalid(form)

class TechnicienDeleteView(LoginRequiredMixin, DeleteView):
    model = Technicien
    template_name = 'app_techniciens/technicien_confirm_delete.html'
    success_url = reverse_lazy('app_techniciens:technicien_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Technicien supprimé avec succès.")
        return super().delete(request, *args, **kwargs)
