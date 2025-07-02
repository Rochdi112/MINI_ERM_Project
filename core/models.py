from django.contrib.auth.models import User
from django.db import models

class ProfilUtilisateur(models.Model):
    ROLES = (
        ('admin', 'Administrateur'),
        ('technicien', 'Technicien'),
        ('client', 'Client'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
