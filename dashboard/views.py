from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from app_interventions.models import Intervention
from django.utils import timezone

@login_required
def dashboard_kpi_htmx(request):
    if not getattr(request, 'htmx', False):
        return render(request, 'components/_alert.html', {'type': 'error', 'message': 'Requête non autorisée.'}, status=403)
    user_profile = getattr(request.user, 'profilutilisateur', None)
    qs = Intervention.objects.all()
    if user_profile and user_profile.role == 'technicien':
        qs = qs.filter(technicien__nom=request.user.username)
    total = qs.count()
    en_retard = qs.filter(statut='en_cours', date__lt=timezone.now().date()).count()
    a_venir = qs.filter(date__gt=timezone.now().date()).count()
    return render(request, 'dashboard/_kpi_fragment.html', {
        'total': total,
        'en_retard': en_retard,
        'a_venir': a_venir,
    })
