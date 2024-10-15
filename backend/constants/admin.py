from django.contrib import admin
from .models import Constant, RepMonth, Unit,Update

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