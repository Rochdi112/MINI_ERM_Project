from django.db import models
from app_interventions.models import Intervention

class Rapport(models.Model):
    intervention = models.OneToOneField(Intervention, on_delete=models.CASCADE, related_name="rapport", verbose_name="Intervention")
    contenu = models.TextField(verbose_name="Contenu du rapport", blank=False, null=False)
    fichier_pdf = models.FileField(upload_to='rapports/', null=True, blank=True, verbose_name="Fichier PDF")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    class Meta:
        verbose_name = "Rapport"
        verbose_name_plural = "Rapports"

    def __str__(self):
        return f"Rapport pour {self.intervention}"
