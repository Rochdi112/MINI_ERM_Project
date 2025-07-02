from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_interventions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rapport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenu', models.TextField()),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('fichier_pdf', models.FileField(blank=True, null=True, upload_to='rapports/')),
                ('intervention', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app_interventions.intervention')),
            ],
        ),
    ]
