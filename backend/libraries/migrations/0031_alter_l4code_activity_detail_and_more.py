# Generated by Django 5.0.7 on 2024-08-02 07:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0030_alter_l1code_code_comb_alter_l2code_code_comb_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='l4code',
            name='activity_detail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='libraries.activitytypedetail', verbose_name='Income Activity Type Detail'),
        ),
        migrations.AlterField(
            model_name='l4code',
            name='activity_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='libraries.activitytype', verbose_name='Income Activity Type'),
        ),
        migrations.AlterField(
            model_name='l4code',
            name='mtc_dgs_nkt',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
