from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Rapport
import os

@receiver(post_delete, sender=Rapport)
def delete_rapport_pdf(sender, instance, **kwargs):
    if instance.fichier_pdf and instance.fichier_pdf.name:
        if os.path.isfile(instance.fichier_pdf.path):
            instance.fichier_pdf.delete(save=False)
