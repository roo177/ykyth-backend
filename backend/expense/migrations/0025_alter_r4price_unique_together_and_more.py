# Generated by Django 5.0.7 on 2024-08-11 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constants', '0005_rename_updates_update_alter_update_table'),
        ('expense', '0024_r4price_operator_m2_code_r4price_operator_t1_code'),
        ('libraries', '0041_alter_t1code_unique_together_t1code_code_comb_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='r4price',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='r4price',
            name='price_adjustment_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='r4price',
            unique_together={('r4_code', 'rep_month', 'm2_code', 't1_code', 'price_adjustment_type')},
        ),
    ]
