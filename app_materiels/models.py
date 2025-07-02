from django.db import models

class Materiel(models.Model):
    nom = models.CharField(max_length=100)
    reference = models.CharField(max_length=100)
    marque = models.CharField(max_length=100)
    date_installation = models.DateField()

    def __str__(self):
        return f"{self.nom} - {self.reference}"
