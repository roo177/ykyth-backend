# Generated by Django 3.2.20 on 2023-09-03 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_import_export', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileimportexportstatus',
            name='file_process_type',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
