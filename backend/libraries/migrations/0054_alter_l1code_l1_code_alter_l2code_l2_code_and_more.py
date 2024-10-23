# Generated by Django 5.0.7 on 2024-10-18 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0053_remove_r4code_fin_model_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='l1code',
            name='l1_code',
            field=models.CharField(max_length=1),
        ),
        migrations.AlterField(
            model_name='l2code',
            name='l2_code',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='l3code',
            name='l3_code',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='l4code',
            name='l4_code',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='t1code',
            name='price_adjustment',
            field=models.CharField(blank=True, choices=[('FFK AK', 'FFK AK'), ('YKT AK', 'YKT AK'), ('BKM AK', 'BKM AK'), ('EUR AK', 'EUR AK'), ('USD AK', 'USD AK'), ('DGS.01', 'DGS.01'), ('DGS.02', 'DGS.02'), ('PTS.01', 'PTS.01'), ('PTS.02', 'PTS.02'), ('RYS.01', 'RYS.01'), ('RYS.02', 'RYS.02'), ('RYS.03', 'RYS.03'), ('OZD.01', 'OZD.01'), ('OZD.02', 'OZD.02'), ('-', '-'), ('GFF AK', 'GFF AK')], max_length=100, null=True),
        ),
    ]