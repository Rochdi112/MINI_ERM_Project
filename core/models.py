from django.db import models
from django.contrib.auth.models import User

class ProfilUtilisateur(models.Model):
    ROLE_ADMIN = 'admin'
    ROLE_TECH = 'technicien'
    ROLE_CLIENT = 'client'
    ROLE_CHEF_PROJET = 'chef_projet'

    ROLE_CHOICES = (
        (ROLE_ADMIN, 'Administrateur'),
        (ROLE_TECH, 'Technicien'),
        (ROLE_CLIENT, 'Client'),
        (ROLE_CHEF_PROJET, 'Chef de projet'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profilutilisateur')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
