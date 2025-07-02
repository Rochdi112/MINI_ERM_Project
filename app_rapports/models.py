from django.db import models
from app_interventions.models import Intervention

class Rapport(models.Model):
    intervention = models.OneToOneField(Intervention, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    fichier_pdf = models.FileField(upload_to='rapports/', null=True, blank=True)

    def __str__(self):
        return f"Rapport Intervention #{self.intervention.id}"
