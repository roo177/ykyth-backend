# Generated by Django 5.0.7 on 2024-10-15 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0043_r4price_fin_model_r4price_fin_model_ratio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='r4price',
            name='fin_model',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]