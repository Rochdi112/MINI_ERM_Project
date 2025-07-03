from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Rapport
from .forms import RapportForm
from core.models import ProfilUtilisateur
from django.http import HttpResponse, HttpResponseForbidden
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
import logging
from django.contrib.auth.decorators import login_required
from django.conf import settings
from app_interventions.models import Attachment

logger = logging.getLogger(__name__)

class RapportListView(LoginRequiredMixin, ListView):
    model = Rapport
    template_name = 'app_rapports/rapport_list.html'
    context_object_name = 'rapports'

    def get_queryset(self):
        user_profile = getattr(self.request.user, 'profilutilisateur', None)
        qs = super().get_queryset()
        # Exemple de filtrage par rôle (à adapter selon la logique métier)
        if user_profile and user_profile.role == 'technicien':
            return qs.filter(intervention__technicien__nom=self.request.user.username)
        return qs

class RapportCreateView(LoginRequiredMixin, CreateView):
    model = Rapport
    form_class = RapportForm
    template_name = 'app_rapports/rapport_form.html'
    success_url = reverse_lazy('app_rapports:rapport_list')

    def form_valid(self, form):
        messages.success(self.request, "Rapport créé avec succès.")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, "Erreur lors de la création du rapport.")
        return super().form_invalid(form)

class RapportUpdateView(LoginRequiredMixin, UpdateView):
    model = Rapport
    form_class = RapportForm
    template_name = 'app_rapports/rapport_form.html'
    success_url = reverse_lazy('app_rapports:rapport_list')

    def form_valid(self, form):
        messages.success(self.request, "Rapport modifié avec succès.")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, "Erreur lors de la modification du rapport.")
        return super().form_invalid(form)

class RapportDeleteView(LoginRequiredMixin, DeleteView):
    model = Rapport
    template_name = 'app_rapports/rapport_confirm_delete.html'
    success_url = reverse_lazy('app_rapports:rapport_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Rapport supprimé avec succès.")
        return super().delete(request, *args, **kwargs)

@login_required
def rapport_pdf(request, pk):
    rapport = get_object_or_404(Rapport, pk=pk)
    intervention = rapport.intervention
    checklist = intervention.checklist_items.all()
    # Inclure tous les fichiers joints (Attachment + FichierJoint)
    attachments = list(intervention.attachments.all()) + list(getattr(intervention, 'fichiers_joints', []).all() if hasattr(intervention, 'fichiers_joints') else [])
    signature_url = intervention.signature_path.url if intervention.signature_path else None
    html_string = render_to_string('app_rapports/rapport_pdf_template.html', {
        'rapport': rapport,
        'intervention': intervention,
        'checklist': checklist,
        'attachments': attachments,
        'signature_url': signature_url,
    })
    with tempfile.NamedTemporaryFile(delete=True) as output:
        HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf(output.name)
        output.seek(0)
        response = HttpResponse(output.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'filename=rapport_{rapport.pk}.pdf'
        return response

@login_required
def generate_pdf(request, pk):
    rapport = get_object_or_404(Rapport, pk=pk)
    # Création auto du profil si absent
    if not hasattr(request.user, 'profilutilisateur'):
        from core.models import ProfilUtilisateur
        ProfilUtilisateur.objects.create(user=request.user, role='admin')
    user_profile = getattr(request.user, 'profilutilisateur', None)
    is_technicien = False
    if rapport.intervention.technicien and hasattr(rapport.intervention.technicien, 'user'):
        is_technicien = rapport.intervention.technicien.user_id == request.user.id
    if not (user_profile and (user_profile.role == 'admin' or is_technicien)):
        return HttpResponseForbidden("Accès refusé.")
    try:
        # Nettoyage ancien PDF si existant
        if rapport.fichier_pdf:
            rapport.fichier_pdf.delete(save=False)
        html_string = render_to_string('app_rapports/rapport_pdf_template.html', {'rapport': rapport})
        html = HTML(string=html_string)
        with tempfile.NamedTemporaryFile(delete=True, suffix='.pdf') as result:
            html.write_pdf(target=result.name)
            rapport.fichier_pdf.save(f"rapport_{rapport.id}.pdf", result)
            rapport.save()
            result.seek(0)
            response = HttpResponse(result.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename=rapport_{rapport.id}.pdf'
            messages.success(request, "PDF généré avec succès.")
            return response
    except Exception as e:
        logger.error(f"Erreur génération PDF : {e}")
        messages.error(request, "Erreur lors de la génération du PDF.")
        return redirect('app_rapports:rapport_detail', pk=pk)
