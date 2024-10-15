# Generated by Django 5.0.7 on 2024-08-07 18:34

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constants', '0005_rename_updates_update_alter_update_table'),
        ('expense', '0020_expenseanalysis_m2_code_expenseanalysis_t1_code_and_more'),
        ('libraries', '0035_r4code_machine_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MachineryList',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('machine_qty', models.FloatField(default=1)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created_set', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_deleted_set', to=settings.AUTH_USER_MODEL)),
                ('r4_code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='libraries.r4code', verbose_name='Expense_r4_code')),
                ('rep_month', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='constants.repmonth', verbose_name='Expense_rep_month')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 't_exp_machinery_list',
                'ordering': ['r4_code'],
            },
        ),
    ]
