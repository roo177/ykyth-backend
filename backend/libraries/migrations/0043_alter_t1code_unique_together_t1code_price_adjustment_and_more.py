# Generated by Django 5.0.7 on 2024-08-11 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0042_alter_t1code_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='t1code',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='t1code',
            name='price_adjustment',
            field=models.CharField(blank=True, choices=[('FFK AK', 'FFK AK'), ('YKT AK', 'YKT AK'), ('BKM AK', 'BKM AK'), ('EUR AK', 'EUR AK'), ('USD AK', 'USD AK'), ('DOĞUŞ TEKNİK', 'DOĞUŞ TEKNİK'), ('DOĞUŞ TEKNİK Y.01', 'DOĞUŞ TEKNİK Y.01'), ('-', '-')], max_length=100, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='t1code',
            unique_together={('t1_code', 'price_adjustment')},
        ),
    ]
