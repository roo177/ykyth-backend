# Generated by Django 5.0.7 on 2024-07-23 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('income', '0002_incomequantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incomequantity',
            name='income_activity_type',
        ),
        migrations.RemoveField(
            model_name='incomeactivitytypedetail',
            name='income_activity_type',
        ),
        migrations.RemoveField(
            model_name='incomeactivitytypedetail',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='incomeactivitytypedetail',
            name='deleted_by',
        ),
        migrations.RemoveField(
            model_name='incomeactivitytypedetail',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='incomequantity',
            name='income_activity_type_detail',
        ),
        migrations.DeleteModel(
            name='IncomeActivityType',
        ),
        migrations.DeleteModel(
            name='IncomeActivityTypeDetail',
        ),
    ]
