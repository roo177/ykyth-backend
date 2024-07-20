
from django.contrib import admin
from .models import L1Code, L2Code, L3Code, L4Code
from constants.models import Unit

class CommonAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('is_active', 'is_deleted', 'created_by', 'updated_by', 'deleted_by')
    search_fields = ('id',)
    list_display = ('id', 'is_active', 'is_deleted', 'created_at', 'updated_at', 'created_by', 'updated_by', 'deleted_by', 'deleted_at')

class L1CodesAdmin(CommonAdmin):
    list_display = ('l1_code', 'description', 'code_comb') + CommonAdmin.list_display
    search_fields = ('l1_code', 'description', 'code_comb')
    list_filter = ('is_active', 'is_deleted')

class L2CodesAdmin(CommonAdmin):
    list_display = ('l2_code', 'l1_code', 'description', 'code_comb') + CommonAdmin.list_display
    search_fields = ('l2_code', 'description', 'l1_code__l1_code')

class L3CodesAdmin(CommonAdmin):
    list_display = ('l3_code', 'l2_code', 'description', 'code_comb') + CommonAdmin.list_display
    search_fields = ('l3_code', 'description', 'l2_code__l2_code')

class L4CodesAdmin(CommonAdmin):
    list_display = ('l4_code', 'l3_code', 'description', 'unit', 'code_comb') + CommonAdmin.list_display
    search_fields = ('l4_code', 'description', 'l3_code__l3_code')
    list_filter = ('is_active', 'is_deleted', 'created_by', 'updated_by', 'deleted_by')


admin.site.register(L4Code, L4CodesAdmin)
admin.site.register(L1Code, L1CodesAdmin)
admin.site.register(L2Code, L2CodesAdmin)
admin.site.register(L3Code, L3CodesAdmin)

