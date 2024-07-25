from django.contrib import admin
from .models import IncomeQuantity

class CommonAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('is_active', 'is_deleted', 'created_by', 'updated_by', 'deleted_by')
    search_fields = ('id',)
    list_display = ('id', 'is_active', 'is_deleted', 'created_at', 'updated_at', 'created_by', 'updated_by', 'deleted_by', 'deleted_at')

class IncomeQuantityAdmin(CommonAdmin):
    list_display = (
        'rep_month', 
        'l4_code', 
        'inc_month', 
        'inc_qty', 
        'activity_detail'
    ) + CommonAdmin.list_display

    search_fields = (
        'rep_month__rep_month', 
        'l4_code__code_comb', 
        'inc_month', 
        'activity_detail__name'
    )

    list_filter = (
        'is_active', 
        'is_deleted', 
        'created_by', 
        'updated_by', 
        'deleted_by', 
        'rep_month', 
        'l4_code', 
        'inc_month', 
        'activity_detail'
    )

    def __str__(self):
        return f"{self.rep_month.rep_month} - {self.l4_code.code_comb}"

# Register the admin class with the associated model
admin.site.register(IncomeQuantity, IncomeQuantityAdmin)
