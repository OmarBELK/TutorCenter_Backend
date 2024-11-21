# Generated by Django 4.2.16 on 2024-11-21 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school_api', '0013_depense_sortiebanque'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paiement',
            name='commission_percentage',
        ),
        migrations.AddField(
            model_name='groupe',
            name='prix_subscription',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='paiement',
            name='frais_inscription',
            field=models.FloatField(default=100),
        ),
        migrations.AddField(
            model_name='paiement',
            name='montant_total',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='paiement',
            name='remaining',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='groupe',
            name='nom_groupe',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='paiement',
            name='groupe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_api.groupe'),
        ),
        migrations.AlterField(
            model_name='paiement',
            name='montant',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Event',
        ),
    ]
