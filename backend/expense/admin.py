from django.contrib import admin
from .models import R4Price
from expense.models import ExpenseAnalysis
from libraries.admin import CommonAdmin

@admin.register(R4Price)
class R4PriceAdmin(CommonAdmin):
    list_display = (
        'rep_month',
        'r4_code',
        'unit',
        'currency',
        'origin',
        'price',
        'price_date',
        'price_adjustment_type',
        'bool_depreciation',
        'depreciation_type',
        'depreciation_price',
        'energy_type',
        'operator_r4_code',
        'fin_type',
        'customs',
        'content_constant',
        'machine_id',
    )
    list_filter = (
        'rep_month',
        'r4_code',
        'currency',
        'origin',
        'price_date',
        'price_adjustment_type',
        'bool_depreciation',
        'depreciation_type',
        'energy_type',
        'fin_type',
        'customs',
    )
    search_fields = (
        'rep_month__name',  # Assuming RepMonth has a field 'name'
        'r4_code__code_comb',  # Assuming R4Code has a field 'code_comb'
        'unit__name',  # Assuming Unit has a field 'name'
        'currency',
        'origin',
        'price_adjustment_type',
        'depreciation_type',
        'energy_type',
        'operator_r4_code__code_comb',  # Assuming R4Code has a field 'code_comb'
        'fin_type',
        'machine_id',
    )
    ordering = ['rep_month__rep_month', 'r4_code__code_comb']

@admin.register(ExpenseAnalysis)
class ExpenseAnalysisAdmin(CommonAdmin):
    list_display = (
        'rep_month',
        'l4_code',
        'r4_code',
        'r4_desc',
        'work_ratio',
        'work_ratio_desc',
        'output_per_unit_time',
        'output_desc',
        'consumption_per_unit_time',
        'consumption_desc',
    )
    list_filter = (
        'rep_month',
        'l4_code',
        'r4_code',
    )
    search_fields = (
        'rep_month__name',  # Assuming RepMonth has a field 'name'
        'l4_code__code_comb',  # Assuming L4Code has a field 'code_comb'
        'r4_code__code_comb',  # Assuming R4Code has a field 'code_comb'
        'r4_desc',
        'work_ratio_desc',
        'output_desc',
        'consumption_desc',
    )
    ordering = ['rep_month', 'r4_code__code_comb']

    fieldsets = (
        (None, {
            'fields': ('rep_month', 'l4_code', 'r4_code', 'r4_desc')
        }),
        ('Work Ratio', {
            'fields': ('work_ratio', 'work_ratio_desc')
        }),
        ('Output', {
            'fields': ('output_per_unit_time', 'output_desc')
        }),
        ('Consumption', {
            'fields': ('consumption_per_unit_time', 'consumption_desc')
        }),
    )