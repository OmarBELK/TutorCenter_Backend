# Generated by Django 4.2.16 on 2024-10-21 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school_api', '0006_etudiant_adresse_etudiant_contact_urgence_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comission',
            name='groupe',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='school_api.groupe'),
        ),
    ]
