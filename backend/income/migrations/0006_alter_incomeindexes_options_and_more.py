# Generated by Django 5.0.7 on 2024-10-11 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('income', '0005_incomeindexes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='incomeindexes',
            options={'ordering': ['inc_month']},
        ),
        migrations.RemoveField(
            model_name='incomeindexes',
            name='rep_month',
        ),
    ]