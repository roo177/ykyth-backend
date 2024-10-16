# Generated by Django 5.0.7 on 2024-07-29 06:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0008_remove_expenseanalysis_r4_code_self'),
        ('libraries', '0029_alter_l4code_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='r4price',
            name='r4_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='r4_prices', to='libraries.r4code', verbose_name='R4 Code'),
        ),
    ]
