from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import logging
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Intervention, ChecklistItem, Attachment
from .forms import InterventionForm, ChecklistItemForm, AttachmentForm
from core.models import ProfilUtilisateur
from django.views.decorators.http import require_POST
from django.db.models import Q

logger = logging.getLogger(__name__)

# Suppression des anciennes vues CRUD fonctionnelles

# Vues checklist, upload, etc. conservées car elles sont spécifiques et sécurisées
@login_required
def checklist_view(request, intervention_id):
    intervention = get_object_or_404(Intervention, pk=intervention_id)
    items = intervention.checklist_items.all()
    if request.method == 'POST':
        form = ChecklistItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.intervention = intervention
            item.save()
            return redirect('app_interventions:checklist', intervention_id=intervention.id)
    else:
        form = ChecklistItemForm()
    return render(request, 'app_interventions/checklist.html', {'intervention': intervention, 'items': items, 'form': form})

@login_required
def checklist_item_update(request, pk):
    item = get_object_or_404(ChecklistItem, pk=pk)
    intervention = item.intervention
    user_profile = getattr(request.user, 'profilutilisateur', None)
    if not (user_profile and (user_profile.role == 'admin' or (intervention.technicien and intervention.technicien.nom == request.user.username))):
        messages.error(request, "Accès refusé.")
        return HttpResponseForbidden("Vous n'avez pas le droit de modifier cette checklist.")
    if request.method == 'POST':
        form = ChecklistItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Checklist modifiée avec succès.")
            return redirect('app_interventions:checklist', intervention_id=intervention.id)
        else:
            messages.error(request, "Erreur de validation : " + str(form.errors))
    else:
        form = ChecklistItemForm(instance=item)
    return render(request, 'app_interventions/checklist_item_form.html', {'form': form, 'item': item, 'intervention': intervention})

@login_required
def upload_attachment(request, pk):
    intervention = get_object_or_404(Intervention, pk=pk)
    user_profile = getattr(request.user, 'profilutilisateur', None)
    if not (user_profile and (user_profile.role == 'admin' or (intervention.technicien and intervention.technicien.nom == request.user.username))):
        messages.error(request, "Accès refusé.")
        return HttpResponseForbidden("Accès refusé.")
    if request.method == 'POST':
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                attachment = form.save(commit=False)
                attachment.intervention = intervention
                attachment.save()
                messages.success(request, "Fichier uploadé avec succès.")
                return redirect('app_interventions:intervention_detail', pk=pk)
            except Exception as e:
                logger.error(f"Erreur upload fichier : {e}")
                messages.error(request, "Erreur lors de l'upload du fichier.")
        else:
            messages.error(request, "Erreur de validation : " + str(form.errors))
    else:
        form = AttachmentForm()
    attachments = intervention.attachments.all()
    return render(request, 'app_interventions/attachment_upload.html', {'form': form, 'attachments': attachments, 'intervention': intervention})

@login_required
def htmx_upload_attachment(request, pk):
    if not getattr(request, 'htmx', False):
        return render(request, 'components/_alert.html', {'type': 'error', 'message': 'Requête non autorisée.'}, status=403)
    intervention = get_object_or_404(Intervention, pk=pk)
    user_profile = getattr(request.user, 'profilutilisateur', None)
    if not (user_profile and (user_profile.role == 'admin' or (intervention.technicien and intervention.technicien.nom == request.user.username))):
        return render(request, 'components/_alert.html', {'type': 'error', 'message': 'Accès refusé.'}, status=403)
    if request.method == 'POST':
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                attachment = form.save(commit=False)
                attachment.intervention = intervention
                attachment.save()
                return render(request, 'app_interventions/_attachment_item.html', {'attachment': attachment, 'success': True})
            except Exception as e:
                logger.error(f"Erreur upload fichier : {e}")
                return render(request, 'components/_alert.html', {'type': 'error', 'message': "Erreur lors de l'upload du fichier."}, status=500)
        else:
            return render(request, 'components/_alert.html', {'type': 'error', 'message': form.errors.as_text()}, status=400)
    return render(request, 'components/_alert.html', {'type': 'error', 'message': 'Méthode non autorisée.'}, status=405)

@login_required
def htmx_checklist_toggle(request, pk):
    if not getattr(request, 'htmx', False):
        return render(request, 'components/_alert.html', {'type': 'error', 'message': 'Requête non autorisée.'}, status=403)
    item = get_object_or_404(ChecklistItem, pk=pk)
    user_profile = getattr(request.user, 'profilutilisateur', None)
    # Seul admin ou technicien assigné à l'intervention peut modifier
    if not (user_profile and (user_profile.role == 'admin' or (item.intervention.technicien and item.intervention.technicien.nom == request.user.username))):
        return render(request, 'components/_alert.html', {'type': 'error', 'message': 'Accès refusé.'}, status=403)
    try:
        item.completed = not item.completed
        item.save()
        return render(request, 'app_interventions/_checklist_item.html', {'item': item})
    except Exception as e:
        logger.error(f"Erreur toggle checklist : {e}")
        return render(request, 'components/_alert.html', {'type': 'error', 'message': "Erreur lors du changement d'état."}, status=500)

@login_required
def planifier_preventive(request):
    if not request.user.is_superuser:
        messages.error(request, "Accès réservé à l'admin.")
        return HttpResponseForbidden("Accès réservé à l'admin.")
    from app_materiels.models import Materiel
    from django.utils import timezone
    from datetime import timedelta
    try:
        nb_crees = 0
        for materiel in Materiel.objects.all():
            freq = getattr(materiel, 'frequence_maintenance', 180)
            prochaine_date = timezone.now().date() + timedelta(days=freq)
            # Vérifie s'il existe déjà une intervention planifiée pour ce matériel à cette date
            existe = Intervention.objects.filter(materiel=materiel, type='preventive', statut='planifiée', date_creation=prochaine_date).exists()
            if not existe:
                Intervention.objects.create(
                    client=materiel.client,
                    materiel=materiel,
                    technicien=None,
                    type='preventive',
                    statut='planifiée',
                    date_creation=prochaine_date,
                    description='Intervention préventive planifiée automatiquement'
                )
                nb_crees += 1
        messages.success(request, f"{nb_crees} interventions préventives créées.")
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Erreur planification préventive : {e}")
        messages.error(request, "Erreur lors de la planification préventive.")
    return redirect('dashboard')

class InterventionListView(LoginRequiredMixin, ListView):
    model = Intervention
    template_name = 'app_interventions/intervention_list.html'
    context_object_name = 'interventions'

    def get_queryset(self):
        user_profile = getattr(self.request.user, 'profilutilisateur', None)
        qs = super().get_queryset()
        if user_profile and user_profile.role == 'technicien':
            return qs.filter(technicien__nom=self.request.user.username)
        return qs

class InterventionCreateView(LoginRequiredMixin, CreateView):
    model = Intervention
    form_class = InterventionForm
    template_name = 'app_interventions/intervention_form.html'
    success_url = reverse_lazy('app_interventions:intervention_list')

    def form_valid(self, form):
        try:
            messages.success(self.request, "Intervention créée avec succès.")
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Erreur création intervention : {e}")
            messages.error(self.request, "Erreur lors de la création de l'intervention.")
            return self.form_invalid(form)
    def form_invalid(self, form):
        messages.error(self.request, "Erreur lors de la création de l'intervention.")
        return super().form_invalid(form)

class InterventionUpdateView(LoginRequiredMixin, UpdateView):
    model = Intervention
    form_class = InterventionForm
    template_name = 'app_interventions/intervention_form.html'
    success_url = reverse_lazy('app_interventions:intervention_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        user_profile = getattr(request.user, 'profilutilisateur', None)
        if user_profile and user_profile.role == 'technicien' and obj.technicien.nom != request.user.username:
            messages.error(request, "Vous n'avez pas le droit de modifier cette intervention.")
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        try:
            messages.success(self.request, "Intervention modifiée avec succès.")
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Erreur modification intervention : {e}")
            messages.error(self.request, "Erreur lors de la modification de l'intervention.")
            return self.form_invalid(form)
    def form_invalid(self, form):
        messages.error(self.request, "Erreur lors de la modification de l'intervention.")
        return super().form_invalid(form)

class InterventionDeleteView(LoginRequiredMixin, DeleteView):
    model = Intervention
    template_name = 'app_interventions/intervention_confirm_delete.html'
    success_url = reverse_lazy('app_interventions:intervention_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        user_profile = getattr(request.user, 'profilutilisateur', None)
        if user_profile and user_profile.role == 'technicien' and obj.technicien.nom != request.user.username:
            messages.error(request, "Vous n'avez pas le droit de supprimer cette intervention.")
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)
    def delete(self, request, *args, **kwargs):
        try:
            messages.success(request, "Intervention supprimée avec succès.")
            return super().delete(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Erreur suppression intervention : {e}")
            messages.error(request, "Erreur lors de la suppression de l'intervention.")
            return self.get(request, *args, **kwargs)

@login_required
def toggle_checklist_item_htmx(request, pk):
    if not getattr(request, 'htmx', False):
        return render(request, 'components/_alert.html', {'type': 'error', 'message': 'Requête non autorisée.'}, status=403)
    item = get_object_or_404(ChecklistItem, pk=pk)
    user_profile = getattr(request.user, 'profilutilisateur', None)
    if not (user_profile and (user_profile.role == 'admin' or (item.intervention.technicien and item.intervention.technicien.nom == request.user.username))):
        return render(request, 'components/_alert.html', {'type': 'error', 'message': 'Accès refusé.'}, status=403)
    try:
        item.completed = not item.completed
        item.save()
        return render(request, 'app_interventions/_checklist_item.html', {'item': item})
    except Exception as e:
        logger.error(f"Erreur toggle checklist : {e}")
        return render(request, 'components/_alert.html', {'type': 'error', 'message': "Erreur lors du changement d'état."}, status=500)

@login_required
def filter_interventions_htmx(request):
    if not getattr(request, 'htmx', False):
        return render(request, 'components/_alert.html', {'type': 'error', 'message': 'Requête non autorisée.'}, status=403)
    user_profile = getattr(request.user, 'profilutilisateur', None)
    qs = Intervention.objects.all()
    client_id = request.GET.get('client')
    site_id = request.GET.get('site')
    materiel_id = request.GET.get('materiel')
    if client_id:
        qs = qs.filter(client_id=client_id)
    if site_id:
        qs = qs.filter(site_id=site_id)
    if materiel_id:
        qs = qs.filter(materiel_id=materiel_id)
    # Filtrage par rôle
    if user_profile and user_profile.role == 'technicien':
        qs = qs.filter(technicien__nom=request.user.username)
    return render(request, 'app_interventions/_filter_select.html', {'interventions': qs})

@login_required
def modal_form_intervention_htmx(request):
    if not getattr(request, 'htmx', False):
        return render(request, 'components/_alert.html', {'type': 'error', 'message': 'Requête non autorisée.'}, status=403)
    user_profile = getattr(request.user, 'profilutilisateur', None)
    if request.method == 'POST':
        form = InterventionForm(request.POST)
        if form.is_valid():
            intervention = form.save()
            return render(request, 'app_interventions/_intervention_modal_form.html', {'form': InterventionForm(), 'success': True, 'intervention': intervention})
        else:
            return render(request, 'app_interventions/_intervention_modal_form.html', {'form': form, 'success': False})
    else:
        form = InterventionForm()
    return render(request, 'app_interventions/_intervention_modal_form.html', {'form': form, 'success': False})
