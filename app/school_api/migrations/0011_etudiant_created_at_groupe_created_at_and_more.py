# Generated by Django 4.2.16 on 2024-10-24 17:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('school_api', '0010_remove_professeur_comission_fixe_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='etudiant',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='groupe',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='professeur',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
