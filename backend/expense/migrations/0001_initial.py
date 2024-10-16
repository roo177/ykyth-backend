# Generated by Django 5.0.7 on 2024-07-28 11:42

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('constants', '0005_rename_updates_update_alter_update_table'),
        ('libraries', '0026_delete_r4price'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='R4Price',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('price', models.FloatField()),
                ('price_date', models.DateField()),
                ('price_adjustment_type', models.CharField(choices=[('FFK AK', 'FFK AK'), ('YKT AK', 'YKT AK'), ('BKM AK', 'BKM AK'), ('EUR AK', 'EUR AK'), ('USD AK', 'USD AK'), ('-', '-')], default='-', max_length=100)),
                ('bool_depreciation', models.BooleanField(default=False)),
                ('depreciation_type', models.CharField(choices=[('MAKİNE', 'MAKİNE'), ('SABİT TESİS', 'SABİT TESİS'), ('ARAÇ', 'ARAÇ'), ('DİĞER EKİPMANLAR', 'DİĞER EKİPMANLAR'), ('-', '-')], default='-', max_length=100)),
                ('energy_type', models.CharField(choices=[('ELEKTRİK', 'ELEKTRİK'), ('DOĞALGAZ', 'DOĞALGAZ'), ('BUHAR', 'BUHAR'), ('MAZOT', 'MAZOT'), ('-', '-')], default='-', max_length=100)),
                ('fin_type', models.CharField(blank=True, choices=[('Sell & LB', 'Sell & LB'), ('Leasing', 'Leasing'), ('Nakit', 'Nakit')], max_length=100, null=True)),
                ('customs', models.BooleanField(default=False)),
                ('currency', models.CharField(blank=True, choices=[('EUR', 'EUR'), ('USD', 'USD'), ('TRY', 'TRY')], max_length=3, null=True)),
                ('origin', models.CharField(blank=True, choices=[('TR', 'TR'), ('OECD', 'OECD'), ('OEKB', 'OEKB'), ('SACE', 'SACE'), ('UKEF', 'UKEF')], max_length=100, null=True)),
                ('content_constant', models.FloatField()),
                ('machine_id', models.CharField(blank=True, max_length=100, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created_set', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_deleted_set', to=settings.AUTH_USER_MODEL)),
                ('operator_r4_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='operator_r4_prices', to='libraries.r4code', verbose_name='Operator R4 Code')),
                ('r4_code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='r4_prices', to='libraries.r4code', verbose_name='R4 Code')),
                ('rep_month', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='constants.repmonth', verbose_name='Reporting Month')),
                ('unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='constants.unit', verbose_name='Unit')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 't_r4_price',
                'ordering': ['price_date'],
                'unique_together': {('r4_code', 'rep_month')},
            },
        ),
    ]
