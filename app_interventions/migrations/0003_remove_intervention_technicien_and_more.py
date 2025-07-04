# Generated by Django 5.2.4 on 2025-07-03 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_interventions', '0002_alter_intervention_options_intervention_date_and_more'),
        ('app_techniciens', '0004_technicien_telephone_technicien_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='intervention',
            name='technicien',
        ),
        migrations.AddField(
            model_name='intervention',
            name='techniciens',
            field=models.ManyToManyField(related_name='interventions', to='app_techniciens.technicien', verbose_name='Techniciens'),
        ),
        migrations.AlterField(
            model_name='intervention',
            name='statut',
            field=models.CharField(choices=[('en_attente', 'En attente'), ('en_cours', 'En cours'), ('terminee', 'Terminée'), ('annulee', 'Annulée')], default='en_attente', max_length=20),
        ),
    ]
