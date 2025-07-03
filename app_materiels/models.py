from django.db import models
from app_clients.models import Site

class Materiel(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="materiels", verbose_name="Site")
    nom = models.CharField(max_length=100, verbose_name="Nom du matériel", blank=False, null=False)
    reference = models.CharField(max_length=100, verbose_name="Référence", blank=False, null=False)
    marque = models.CharField(max_length=100, verbose_name="Marque", blank=False, null=False)
    date_installation = models.DateField(verbose_name="Date d'installation", blank=False, null=False)

    class Meta:
        verbose_name = "Matériel"
        verbose_name_plural = "Matériels"

    def __str__(self):
        return f"{self.nom} - {self.reference} ({self.site.nom})"
