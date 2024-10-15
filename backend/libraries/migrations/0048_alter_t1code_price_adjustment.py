# Generated by Django 5.0.7 on 2024-08-20 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0047_alter_r1code_options_alter_r2code_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='t1code',
            name='price_adjustment',
            field=models.CharField(blank=True, choices=[('FFK AK', 'FFK AK'), ('YKT AK', 'YKT AK'), ('BKM AK', 'BKM AK'), ('EUR AK', 'EUR AK'), ('USD AK', 'USD AK'), ('DGS.01', 'DGS.01'), ('DGS.02', 'DGS.02'), ('PTS.01', 'PTS.01'), ('PTS.02', 'PTS.02'), ('RYS.01', 'RYS.01'), ('RYS.02', 'RYS.02'), ('OZD.01', 'OZD.01'), ('OZD.02', 'OZD.02'), ('-', '-')], max_length=100, null=True),
        ),
    ]
