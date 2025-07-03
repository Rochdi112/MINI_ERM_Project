from django.db import models
from django.contrib.auth.models import User

class ProfilUtilisateur(models.Model):
    ROLES = [
        ('admin', 'Administrateur'),
        ('technicien', 'Technicien'),
        ('client', 'Client'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profil_utilisateur", verbose_name="Utilisateur")
    role = models.CharField(max_length=20, choices=ROLES, verbose_name="Rôle", blank=False, null=False)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
