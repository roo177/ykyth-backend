# Generated by Django 5.0.7 on 2024-08-06 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0016_machinerylist'),
    ]

    operations = [
        migrations.AddField(
            model_name='r4price',
            name='deprciation_quantity',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='r4price',
            name='energy_consumption',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
