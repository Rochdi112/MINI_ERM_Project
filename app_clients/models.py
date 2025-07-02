from django.db import models

class Client(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.TextField()
    contact = models.CharField(max_length=50)

    def __str__(self):
        return self.nom
