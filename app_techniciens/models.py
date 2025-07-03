from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

class Technicien(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    nom = models.CharField(max_length=100, verbose_name="Nom", blank=False, null=False)
    email = models.EmailField(verbose_name="Email", blank=False, null=False, unique=True)
    telephone = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^\+?\d{10,15}$')],
        verbose_name="Téléphone",
        blank=True,
        null=True
    )
    specialite = models.CharField(max_length=100, verbose_name="Spécialité", blank=False, null=False)

    class Meta:
        verbose_name = "Technicien"
        verbose_name_plural = "Techniciens"

    def __str__(self):
        return f"{self.nom} ({self.specialite})"
