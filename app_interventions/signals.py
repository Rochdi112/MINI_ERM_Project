from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

# Le signal est désactivé car le modèle Attachment n'existe pas
# @receiver(post_delete, sender=Attachment)
# def delete_attachment_file(sender, instance, **kwargs):
#     if instance.file and instance.file.name:
#         if os.path.isfile(instance.file.path):
#             instance.file.delete(save=False)
