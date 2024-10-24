# Generated by Django 5.0.7 on 2024-10-11 06:38

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constants', '0005_rename_updates_update_alter_update_table'),
        ('income', '0004_incomequantity_activity_detail'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='IncomeIndexes',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('inc_month', models.DateField()),
                ('inc_index', models.FloatField(default=0)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created_set', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_deleted_set', to=settings.AUTH_USER_MODEL)),
                ('rep_month', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='constants.repmonth', verbose_name='income_rep_month')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 't_inc_index',
                'ordering': ['rep_month', 'inc_month'],
            },
        ),
    ]
