from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
from .models import FichierJoint

# Le signal est désactivé car le modèle Attachment n'existe pas
# @receiver(post_delete, sender=Attachment)
# def delete_attachment_file(sender, instance, **kwargs):
#     if instance.file and instance.file.name:
#         if os.path.isfile(instance.file.path):
#             instance.file.delete(save=False)

@receiver(post_delete, sender=FichierJoint)
def delete_file(sender, instance, **kwargs):
    if instance.fichier:
        instance.fichier.delete(save=False)
