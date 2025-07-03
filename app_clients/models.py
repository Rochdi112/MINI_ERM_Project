from django.db import models

class Client(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom", blank=False, null=False)
    email = models.EmailField(verbose_name="Email", blank=False, null=False)
    telephone = models.CharField(max_length=30, verbose_name="Téléphone", blank=False, null=False)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.nom

class Site(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="sites", verbose_name="Client")
    nom = models.CharField(max_length=100, verbose_name="Nom du site", blank=False, null=False)
    adresse = models.CharField(max_length=255, verbose_name="Adresse", blank=False, null=False)

    class Meta:
        verbose_name = "Site"
        verbose_name_plural = "Sites"

    def __str__(self):
        return f"{self.nom} ({self.client.nom})"
