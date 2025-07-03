from django.db import models

class Technicien(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom")
    email = models.EmailField(verbose_name="Email")
    specialite = models.CharField(max_length=100, verbose_name="Spécialité")

    class Meta:
        verbose_name = "Technicien"
        verbose_name_plural = "Techniciens"

    def __str__(self):
        return f"{self.nom} ({self.specialite})"
