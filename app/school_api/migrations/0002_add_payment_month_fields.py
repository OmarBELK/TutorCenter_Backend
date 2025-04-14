from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('school_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paiement',
            name='mois_paiement',
            field=models.CharField(default='2025-01', max_length=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comission',
            name='mois_comission',
            field=models.CharField(default='2025-01', max_length=7),
            preserve_default=False,
        ),
    ]
