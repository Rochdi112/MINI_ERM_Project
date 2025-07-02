from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_clients', '0001_initial'),
        ('app_techniciens', '0001_initial'),
        ('app_materiels', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Intervention',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('corrective', 'Corrective'), ('preventive', 'Préventive')], max_length=20)),
                ('statut', models.CharField(choices=[('en_attente', 'En attente'), ('en_cours', 'En cours'), ('terminee', 'Terminée')], default='en_attente', max_length=20)),
                ('date_creation', models.DateField(auto_now_add=True)),
                ('date_cloture', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_clients.client')),
                ('materiel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_materiels.materiel')),
                ('technicien', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_techniciens.technicien')),
            ],
        ),
    ]
