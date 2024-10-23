from django.contrib import admin
from .models import Constant, RepMonth, Unit,Update,Month

@admin.register(Constant)
class ConstantsAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'description')
    search_fields = ('key', 'value', 'description')
    list_filter = ('key',)

@admin.register(RepMonth)
class RepMonthAdmin(admin.ModelAdmin):
    list_display = ('rep_month', 'month', 'year', 'rep_month_date', 'is_active', 'is_deleted')
    search_fields = ('rep_month',)
    list_filter = ('rep_month_date', 'month', 'year')

@admin.register(Unit)
class UnitsAdmin(admin.ModelAdmin):
    list_display = ('unit', 'description','id', 'is_active', 'is_deleted')
    search_fields = ('unit', 'description')
    list_filter = ('unit', 'description')


class UpdateAdmin(admin.ModelAdmin):
    list_display = ('update', 'description')
    search_fields = ('update', 'description')
    ordering = ('update',)
    
admin.site.register(Update, UpdateAdmin)

class MonthAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('month', 'month_no', 'year_no', 'is_active', 'created_by', 'updated_by', 'deleted_by', 'created_at', 'updated_at')
    
    # Fields to use for searching
    search_fields = ('month_no', 'year_no', 'created_by__username', 'updated_by__username', 'deleted_by__username')
    
    # Fields to filter by in the admin list view
    list_filter = ('month_no', 'year_no', 'is_active', 'is_deleted', 'created_by', 'updated_by')
    
    # Read-only fields (for fields that should not be editable)
    readonly_fields = ('created_at', 'updated_at', 'deleted_at', 'created_by', 'updated_by', 'deleted_by')

    # Automatically set the `created_by` and `updated_by` fields based on the current user
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If it's a new object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    # Customize the form view
    fieldsets = (
        (None, {
            'fields': ('month', 'month_no', 'year_no', 'is_active')
        }),
        ('Audit Info', {
            'fields': ('created_by', 'updated_by', 'deleted_by', 'created_at', 'updated_at', 'deleted_at'),
            'classes': ('collapse',),
        }),
    )

# Register the Month model with the custom admin
admin.site.register(Month, MonthAdmin)