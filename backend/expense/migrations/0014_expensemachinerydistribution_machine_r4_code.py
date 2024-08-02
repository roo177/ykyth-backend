# Generated by Django 5.0.7 on 2024-07-30 14:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0013_expensemachinerydistribution_expensequantity'),
        ('libraries', '0029_alter_l4code_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='expensemachinerydistribution',
            name='machine_r4_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='machine_r4_code', to='libraries.r4code', verbose_name='Machine_r4_code'),
        ),
    ]