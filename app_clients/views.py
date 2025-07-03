from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Client
from .forms import ClientForm
from core.models import ProfilUtilisateur

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'app_clients/client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        user_profile = getattr(self.request.user, 'profilutilisateur', None)
        qs = super().get_queryset()
        # Exemple de filtrage par rôle (à adapter selon la logique métier)
        if user_profile and user_profile.role == 'technicien':
            return qs.none()
        return qs

class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'app_clients/client_form.html'
    success_url = reverse_lazy('app_clients:client_list')

    def form_valid(self, form):
        messages.success(self.request, "Client créé avec succès.")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, "Erreur lors de la création du client.")
        return super().form_invalid(form)

class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'app_clients/client_form.html'
    success_url = reverse_lazy('app_clients:client_list')

    def form_valid(self, form):
        messages.success(self.request, "Client modifié avec succès.")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, "Erreur lors de la modification du client.")
        return super().form_invalid(form)

class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'app_clients/client_confirm_delete.html'
    success_url = reverse_lazy('app_clients:client_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Client supprimé avec succès.")
        return super().delete(request, *args, **kwargs)
