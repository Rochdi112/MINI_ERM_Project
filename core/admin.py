from django.contrib import admin
from .models import ProfilUtilisateur

@admin.register(ProfilUtilisateur)
class ProfilUtilisateurAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
