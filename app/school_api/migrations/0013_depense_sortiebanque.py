# Generated by Django 4.2.16 on 2024-11-08 06:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('school_api', '0012_remove_groupe_commission_fixe_remove_groupe_matiere_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Depense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('libele', models.CharField(max_length=200)),
                ('montant', models.FloatField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='SortieBanque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('mode_paiement', models.CharField(choices=[('CHEQUE', 'Chèque'), ('VIREMENT', 'Virement'), ('ESPECES', 'Espèces'), ('CARTE', 'Carte Bancaire')], max_length=50)),
                ('montant', models.FloatField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
