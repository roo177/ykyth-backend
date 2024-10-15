# Generated by Django 5.0.7 on 2024-08-06 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0032_t1code_y1code_t2code_y2code'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='t1code',
            unique_together={('t1_code',)},
        ),
        migrations.DeleteModel(
            name='T2Code',
        ),
        migrations.RemoveField(
            model_name='t1code',
            name='code_comb',
        ),
    ]
