# Generated by Django 5.0.7 on 2024-08-07 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0034_delete_t2code'),
    ]

    operations = [
        migrations.AddField(
            model_name='r4code',
            name='machine_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]