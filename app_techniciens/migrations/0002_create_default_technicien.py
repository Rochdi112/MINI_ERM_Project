from django.db import migrations

def create_default_technicien(apps, schema_editor):
    Technicien = apps.get_model('app_techniciens', 'Technicien')
    Technicien.objects.get_or_create(
        id=1,
        defaults={
            'nom': 'Technicien par défaut',
            'specialite': 'Généraliste',
            'email': 'tech1@default.com',
        }
    )

class Migration(migrations.Migration):
    dependencies = [
        ('app_techniciens', '0001_initial'),  # À adapter si besoin
    ]
    operations = [
        migrations.RunPython(create_default_technicien),
    ]
