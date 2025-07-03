# signals.py pour suppression future de fichiers (squelette)
from django.db.models.signals import post_delete
from django.dispatch import receiver
# from .models import ... # Ajouter ici les modèles avec fichiers si besoin

# Exemple :
# @receiver(post_delete, sender=MonModeleAvecFichier)
# def delete_file_on_delete(sender, instance, **kwargs):
#     if instance.fichier and instance.fichier.name:
#         instance.fichier.delete(save=False)
