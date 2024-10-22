# Generated by Django 4.2.3 on 2024-10-22 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pgdi_api', '0003_user_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(blank=True, choices=[('contestant', 'Contestant'), ('creator', 'Creator')], default='contestant', max_length=10),
        ),
    ]
