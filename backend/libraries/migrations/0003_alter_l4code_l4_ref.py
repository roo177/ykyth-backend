# Generated by Django 5.0.7 on 2024-07-18 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='l4code',
            name='l4_ref',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
