# Generated by Django 5.0.7 on 2024-07-29 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0007_expenseanalysis_r4_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expenseanalysis',
            name='r4_code_self',
        ),
    ]