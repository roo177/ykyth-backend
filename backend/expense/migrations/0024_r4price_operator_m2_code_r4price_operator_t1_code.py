# Generated by Django 5.0.7 on 2024-08-10 11:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0023_r4price_m2_code_r4price_t1_code'),
        ('libraries', '0038_remove_r4code_m2_code_remove_r4code_t1_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='r4price',
            name='operator_m2_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='operator_m2_prices', to='libraries.m2code', verbose_name='Operator M2 Code'),
        ),
        migrations.AddField(
            model_name='r4price',
            name='operator_t1_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='operator_t1_prices', to='libraries.t1code', verbose_name='Operator T1 Code'),
        ),
    ]
