from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils import timezone
from app_interventions.models import Intervention
from app_techniciens.models import Technicien
from app_materiels.models import Materiel
from app_clients.models import Site
from django.db.models import Count, Q
from django.db import models

@login_required
def dashboard(request):
    interventions = Intervention.objects.all()
    materiels = Materiel.objects.all()
    techniciens = Technicien.objects.all()
    sites = Site.objects.all()

    total_interventions = interventions.count()
    cloturees = interventions.filter(statut='terminee').count()
    taux_cloture = (cloturees / total_interventions * 100) if total_interventions else 0
    techniciens_actifs = techniciens.filter(interventions__isnull=False).distinct().count()
    materiel_par_site = list(sites.annotate(nb_materiel=Count('materiels')).values_list('nom', 'nb_materiel'))
    interventions_par_type = list(interventions.values('type').annotate(count=Count('id')))
    interventions_par_mois = list(
        interventions.extra({'mois': "strftime('%%Y-%%m', date)"}).values('mois').annotate(count=Count('id')).order_by('mois')
    )
    en_cours = interventions.filter(statut='en_cours').count()
    annulees = interventions.filter(statut='annulee').count()
    moyenne_duree = None
    if total_interventions:
        durees = interventions.exclude(date_cloture__isnull=True).annotate(
            duree=(models.F('date_cloture') - models.F('date_creation'))
        ).values_list('duree', flat=True)
        if durees:
            moyenne_duree = sum([d.days for d in durees if hasattr(d, 'days')]) / len(durees)

    context = {
        'total_interventions': total_interventions,
        'taux_cloture': taux_cloture,
        'techniciens_actifs': techniciens_actifs,
        'materiel_par_site': materiel_par_site,
        'interventions_par_type': interventions_par_type,
        'interventions_par_mois': interventions_par_mois,
        'en_cours': en_cours,
        'annulees': annulees,
        'moyenne_duree': moyenne_duree,
    }
    return render(request, 'dashboard/dashboard.html', context)

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
