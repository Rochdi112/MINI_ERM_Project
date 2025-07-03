from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ProfilUtilisateur

@receiver(post_save, sender=User)
def create_profil_utilisateur(sender, instance, created, **kwargs):
    if created:
        # Par défaut, on crée un profil 'client'
        ProfilUtilisateur.objects.create(user=instance, role=ProfilUtilisateur.ROLE_CLIENT)

@receiver(post_save, sender=User)
def save_profil_utilisateur(sender, instance, **kwargs):
    if hasattr(instance, 'profilutilisateur'):
        instance.profilutilisateur.save()
