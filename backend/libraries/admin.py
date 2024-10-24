
from django.contrib import admin
from .models import L1Code, L2Code, L3Code, L4Code,ActivityTypeDetailIncome
from constants.models import Unit
from .models import R1Code, R2Code, R3Code, R4Code
from .models import M1Code, M2Code, T1Code
class CommonAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('is_active', 'is_deleted', 'created_by', 'updated_by', 'deleted_by')
    search_fields = ('id',)
    list_display = ('id', 'is_active', 'is_deleted', 'created_at', 'updated_at')

class L1CodesAdmin(CommonAdmin):
    list_display = ('l1_code', 'description', 'code_comb') + CommonAdmin.list_display
    search_fields = ('l1_code', 'description', 'code_comb')
    list_filter = ('is_active', 'is_deleted')
    ordering = ('code_comb',)  # Add code_comb to ordering
    list_editable = ('code_comb',)  # Make code_comb editable

    ordering = ('-created_at',)  # Add code_comb to ordering
class L2CodesAdmin(CommonAdmin):
    list_display = ('l2_code', 'l1_code', 'description', 'code_comb') + CommonAdmin.list_display
    search_fields = ('l2_code', 'description', 'l1_code__l1_code')
    ordering = ('code_comb',)  # Add code_comb to ordering
    list_editable = ('code_comb',)  # Make code_comb editable

    ordering = ('-created_at',)  # Add code_comb to ordering
class L3CodesAdmin(CommonAdmin):
    list_display = ('l3_code', 'l2_code', 'description', 'code_comb') + CommonAdmin.list_display
    search_fields = ('l3_code', 'description', 'l2_code__l2_code')
    ordering = ('code_comb',)  # Add code_comb to ordering
    list_editable = ('code_comb',)  # Make code_comb editable

    ordering = ('-created_at',)  # Add code_comb to ordering
class L4CodesAdmin(CommonAdmin):
    list_display = (
        'code_comb', 
        'description', 


        'unit', 

        'l4_code', 
        'l3_code', 
        'mtc_dgs_nkt', 
        'nak_ote', 
        'l4_ref', 
        'l4_hkds', 
        'l4_calc_method', 
        'l4_bf_dg', 
        'l4_mk_ks', 
        'tax', 
        'aygm_code', 
        'aygm_group', 
        'aygm_desc', 

        'activity_type', 
        'activity_detail', 
        'l4_order_ratio', 
        'l4_delivery_ratio', 
        'l4_handover_ratio'
    ) + CommonAdmin.list_display

    search_fields = (
        'l4_code',  # Remove __code_comb
        'description', 
        'aygm_code', 
        'aygm_group', 
        'code_comb',
    )


    list_filter = (
        'unit', 
        'l3_code__code_comb',
    )

    ordering = ('-created_at',)  # Add code_comb to ordering


admin.site.register(L4Code, L4CodesAdmin)
admin.site.register(L1Code, L1CodesAdmin)
admin.site.register(L2Code, L2CodesAdmin)
admin.site.register(L3Code, L3CodesAdmin)

from .models import ActivityType, ActivityTypeDetail


@admin.register(ActivityType)
class IncomeActivityTypeAdmin(admin.ModelAdmin):
    list_display = ('description', 'created_at', 'updated_at', 'is_active', 'is_deleted')
    list_filter = ('is_active', 'is_deleted')
    search_fields = ('description',)
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by', 'deleted_by', 'deleted_at')

@admin.register(ActivityTypeDetail)
class IncomeActivityTypeDetailAdmin(admin.ModelAdmin):
    list_display = ('description', 'created_at', 'updated_at', 'is_active', 'is_deleted')
    list_filter = ('is_active', 'is_deleted')
    search_fields = ('description',)
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by', 'deleted_by', 'deleted_at')



class ActivityTypeDetailIncomeAdmin(CommonAdmin):
    list_display = ('description',) + CommonAdmin.list_display
    search_fields = ('description',)
    list_filter = ('is_active', 'is_deleted', 'created_by', 'updated_by', 'deleted_by')

    def __str__(self):
        return self.description

# Register the admin class with the associated model
admin.site.register(ActivityTypeDetailIncome, ActivityTypeDetailIncomeAdmin)

@admin.register(R1Code)
class R1CodeAdmin(CommonAdmin):
    list_display = ('r1_code', 'description', 'code_comb') + CommonAdmin.list_display
    search_fields = ('r1_code', 'description', 'code_comb')
    list_filter = ('is_active', 'is_deleted') + CommonAdmin.list_filter

    ordering = ('-created_at',)  # Add code_comb to ordering
@admin.register(R2Code)
class R2CodeAdmin(CommonAdmin):
    list_display = ('r2_code', 'r1_code', 'description', 'code_comb') + CommonAdmin.list_display
    search_fields = ('r2_code', 'r1_code__r1_code', 'description', 'code_comb')
    list_filter = ('is_active', 'is_deleted') + CommonAdmin.list_filter

    ordering = ('-created_at',)  # Add code_comb to ordering
@admin.register(R3Code)
class R3CodeAdmin(CommonAdmin):
    list_display = ('r3_code', 'r2_code', 'description', 'code_comb') + CommonAdmin.list_display
    search_fields = ('r3_code', 'r2_code__r2_code', 'description', 'code_comb')
    list_filter = ('is_active', 'is_deleted') + CommonAdmin.list_filter

    ordering = ('-created_at',)  # Add code_comb to ordering
@admin.register(R4Code)
class R4CodeAdmin(CommonAdmin):
    list_display = ('r4_code', 'r3_code', 'description', 'code_comb', 'machine_id') + CommonAdmin.list_display
    search_fields = ('r4_code', 'r3_code__r3_code', 'description', 'code_comb')
    list_filter = ('is_active', 'is_deleted') + CommonAdmin.list_filter
    list_editable = ('machine_id',)
@admin.register(M1Code)
class M1CodeAdmin(CommonAdmin):
    list_display = ('m1_code', 'description', 'code_comb') + CommonAdmin.list_display
    search_fields = ('m1_code', 'description', 'code_comb')
    list_filter = ('is_active', 'is_deleted') + CommonAdmin.list_filter

@admin.register(M2Code)
class M2CodeAdmin(CommonAdmin):
    list_display = ('m2_code', 'm1_code', 'description', 'code_comb') + CommonAdmin.list_display
    search_fields = ('m2_code', 'm1_code__m1_code', 'description', 'code_comb')
    list_filter = ('is_active', 'is_deleted') + CommonAdmin.list_filter

@admin.register(T1Code)
class T1CodeAdmin(CommonAdmin):
    list_display = ('t1_code', 'description', 'price_adjustment', 'code_comb') + CommonAdmin.list_display
    search_fields = ('t1_code', 'description', 'price_adjustment', 'code_comb')
    list_filter = ('is_active', 'is_deleted') + CommonAdmin.list_filter