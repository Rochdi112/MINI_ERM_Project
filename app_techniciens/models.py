from django.db import models

class Technicien(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    specialite = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom} ({self.specialite})"
