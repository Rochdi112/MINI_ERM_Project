from django.core.management.base import BaseCommand
from django.utils import timezone
from app_interventions.models import Intervention
from app_materiels.models import Materiel
from app_clients.models import Client, Site
from app_techniciens.models import Technicien
from django.conf import settings
from datetime import timedelta

# À adapter selon votre logique métier
FREQUENCE_JOURS = 30  # Générer une intervention préventive tous les 30 jours

class Command(BaseCommand):
    help = 'Planifie automatiquement les interventions préventives pour chaque matériel.'

    def handle(self, *args, **options):
        today = timezone.now().date()
        for materiel in Materiel.objects.all():
            # Vérifier la dernière intervention préventive
            last_preventive = (
                Intervention.objects.filter(materiel=materiel, type='preventive')
                .order_by('-date')
                .first()
            )
            if not last_preventive or (today - last_preventive.date).days >= FREQUENCE_JOURS:
                # Créer une nouvelle intervention préventive
                intervention = Intervention.objects.create(
                    client=materiel.site.client,
                    materiel=materiel,
                    technicien=Technicien.objects.first(),  # À adapter (ex : technicien assigné par défaut)
                    site=materiel.site,
                    type='preventive',
                    statut='en_attente',
                    date=today + timedelta(days=1),
                    description='Intervention préventive planifiée automatiquement.'
                )
                self.stdout.write(self.style.SUCCESS(f"Intervention préventive créée pour {materiel.nom} (site {materiel.site.nom})"))
            else:
                self.stdout.write(f"Aucune intervention à planifier pour {materiel.nom}")
