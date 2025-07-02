from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Materiel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('reference', models.CharField(max_length=100)),
                ('marque', models.CharField(max_length=100)),
                ('date_installation', models.DateField()),
            ],
        ),
    ]
