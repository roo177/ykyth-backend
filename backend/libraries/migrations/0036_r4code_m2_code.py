# Generated by Django 5.0.7 on 2024-08-10 10:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0035_r4code_machine_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='r4code',
            name='m2_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='libraries.m2code', verbose_name='M2 Code'),
        ),
    ]