from django.db import models

class Technicien(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom", blank=False, null=False)
    email = models.EmailField(verbose_name="Email", blank=False, null=False)
    specialite = models.CharField(max_length=100, verbose_name="Spécialité", blank=False, null=False)

    class Meta:
        verbose_name = "Technicien"
        verbose_name_plural = "Techniciens"

    def __str__(self):
        return f"{self.nom} ({self.specialite})"
