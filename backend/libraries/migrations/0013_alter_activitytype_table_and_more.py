# Generated by Django 5.0.7 on 2024-07-23 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0012_alter_l4code_unique_together'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='activitytype',
            table='t_act_type',
        ),
        migrations.AlterModelTable(
            name='activitytypedetail',
            table='t_act_type_detail',
        ),
    ]
