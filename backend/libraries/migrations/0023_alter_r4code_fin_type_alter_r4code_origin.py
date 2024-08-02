# Generated by Django 5.0.7 on 2024-07-26 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0022_alter_r4code_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='r4code',
            name='fin_type',
            field=models.CharField(blank=True, choices=[('Sell & LB', 'Sell & LB'), ('Leasing', 'Leasing'), ('Nakit', 'Nakit')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='r4code',
            name='origin',
            field=models.CharField(blank=True, choices=[('TR', 'TR'), ('OECD', 'OECD'), ('OEKB', 'OEKB'), ('SACE', 'SACE'), ('UKEF', 'UKEF')], max_length=100, null=True),
        ),
    ]