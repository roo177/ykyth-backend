# Generated by Django 5.0.7 on 2024-09-05 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('constants', '0005_rename_updates_update_alter_update_table'),
        ('expense', '0036_alter_expensequantity_unique_together'),
        ('libraries', '0050_alter_t1code_options'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='expenseanalysis',
            unique_together={('rep_month', 'l4_code', 'r4_code', 'r4_desc', 'r3_code_machine', 'm2_code', 't1_code', 'r3_currency')},
        ),
    ]