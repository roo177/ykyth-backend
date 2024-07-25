from django.contrib import admin
from .models import ActualIndexes, BaseIndex, IndexIncRates

class ActualIndexesAdmin(admin.ModelAdmin):
    list_display = (
        'ac_month', 'b01_tufe', 'b02_mineral', 'b03_main_metal', 'b04_other_metal',
        'b05_petrol', 'b06_wood', 'b07_electricity', 'b08_computer', 'b09_ufe',
        'b10_machinery', 'r_usd_try', 'r_eur_try'
    )
    search_fields = ('ac_month',)
    list_filter = ('ac_month',)
    ordering = ('-ac_month',)
    date_hierarchy = 'ac_month'

class BaseIndexAdmin(admin.ModelAdmin):
    list_display = (
        'ac_month', 'b01_tufe', 'b02_mineral', 'b03_main_metal', 'b04_other_metal',
        'b05_petrol', 'b06_wood', 'b07_electricity', 'b08_computer', 'b09_ufe',
        'b10_machinety', 'r_usd_try', 'r_eur_try'
    )
    search_fields = ('ac_month',)
    list_filter = ('ac_month',)
    ordering = ('-ac_month',)
    date_hierarchy = 'ac_month'

class IndexIncRatesAdmin(admin.ModelAdmin):
    list_display = (
        'rep_month', 'ac_month', 'art_ufe', 'art_tufe', 'art_usd_try', 'art_eur_try'
    )
    search_fields = ('ac_month', 'rep_month__name')  # Adjust the field based on RepMonth model
    list_filter = ('ac_month', 'rep_month')
    ordering = ('-ac_month',)
    date_hierarchy = 'ac_month'

# Register the models with the admin site
admin.site.register(ActualIndexes, ActualIndexesAdmin)
admin.site.register(BaseIndex, BaseIndexAdmin)
admin.site.register(IndexIncRates, IndexIncRatesAdmin)
