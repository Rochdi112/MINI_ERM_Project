from django.shortcuts import render, redirect, get_object_or_404
from .models import Rapport
from .forms import RapportForm
from django.http import HttpResponse, HttpResponseForbidden
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.contrib.auth.decorators import login_required
from core.models import ProfilUtilisateur
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

@login_required
def rapport_list(request):
    rapports = Rapport.objects.all()
    return render(request, 'app_rapports/rapport_list.html', {'rapports': rapports})

@login_required
def rapport_create(request):
    if request.method == 'POST':
        form = RapportForm(request.POST)
        if form.is_valid():
            rapport = form.save()
            return redirect('rapport_list')
    else:
        form = RapportForm()
    return render(request, 'app_rapports/rapport_form.html', {'form': form})

@login_required
def rapport_pdf(request, pk):
    rapport = get_object_or_404(Rapport, pk=pk)
    user_profile = ProfilUtilisateur.objects.get(user=request.user)
    # Autorisé si admin ou technicien assigné à l'intervention
    if not (user_profile.role == 'admin' or (rapport.intervention.technicien and rapport.intervention.technicien.nom == request.user.username)):
        return HttpResponseForbidden("Vous n'avez pas accès à ce rapport PDF.")
    html_string = render_to_string('app_rapports/pdf_template.html', {'rapport': rapport})

    html = HTML(string=html_string)
    result = tempfile.NamedTemporaryFile(delete=True)
    html.write_pdf(target=result.name)

    with open(result.name, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename=rapport_{rapport.id}.pdf'
        return response

@login_required
def generate_pdf(request, pk):
    rapport = get_object_or_404(Rapport, pk=pk)
    user_profile = getattr(request.user, 'profilutilisateur', None)
    if not (user_profile and (user_profile.role == 'admin' or (rapport.intervention.technicien and rapport.intervention.technicien.nom == request.user.username))):
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
