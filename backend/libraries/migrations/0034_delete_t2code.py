# Generated by Django 5.0.7 on 2024-08-07 05:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0033_remove_y2code_y1_code_alter_y2code_unique_together_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='T2Code',
        ),
    ]