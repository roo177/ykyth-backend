# Generated by Django 5.0.7 on 2024-08-06 17:02

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0031_alter_l4code_activity_detail_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='T1Code',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('t1_code', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('code_comb', models.CharField(blank=True, max_length=255)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created_set', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_deleted_set', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 't_t1_code',
                'ordering': ['t1_code'],
                'unique_together': {('code_comb',)},
            },
        ),
        migrations.CreateModel(
            name='Y1Code',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('y1_code', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('code_comb', models.CharField(blank=True, max_length=255)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created_set', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_deleted_set', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 't_y1_code',
                'ordering': ['y1_code'],
                'unique_together': {('code_comb',)},
            },
        ),
        migrations.CreateModel(
            name='T2Code',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('t2_code', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('code_comb', models.CharField(blank=True, max_length=255)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created_set', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_deleted_set', to=settings.AUTH_USER_MODEL)),
                ('t1_code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='libraries.t1code', verbose_name='Y1 Code')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 't_t2_code',
                'ordering': ['t2_code'],
                'unique_together': {('code_comb',)},
            },
        ),
        migrations.CreateModel(
            name='Y2Code',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('y2_code', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('code_comb', models.CharField(blank=True, max_length=255)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created_set', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_deleted_set', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated_set', to=settings.AUTH_USER_MODEL)),
                ('y1_code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='libraries.y1code', verbose_name='Y1 Code')),
            ],
            options={
                'db_table': 't_y2_code',
                'ordering': ['y2_code'],
                'unique_together': {('code_comb',)},
            },
        ),
    ]
