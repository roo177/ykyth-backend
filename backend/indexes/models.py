from common.models import Common
from constants.models import Unit,RepMonth
from django.db import models
# Create your models here.

class ActualIndexes(Common):


    ac_month = models.DateField(null=True, blank=True)
    b01_tufe = models.FloatField(null=True, blank=True)
    b02_mineral = models.FloatField(null=True, blank=True)
    b03_main_metal = models.FloatField(null=True, blank=True)
    b04_other_metal = models.FloatField(null=True, blank=True)  
    b05_petrol = models.FloatField(null=True, blank=True)
    b06_wood = models.FloatField(null=True, blank=True)
    b07_electricity = models.FloatField(null=True, blank=True)
    b08_computer = models.FloatField(null=True, blank=True)
    b09_ufe = models.FloatField(null=True, blank=True)
    b10_machinery = models.FloatField(null=True, blank=True)
    r_usd_try = models.FloatField(null=True, blank=True)
    r_eur_try = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['ac_month']
        db_table = 't_indexes_ac'
        unique_together = ['ac_month']

    def __str__(self):
        return str(self.ac_month)
    
class BaseIndex(Common):
    
    ac_month = models.DateField(null=True, blank=True)
    b01_tufe = models.FloatField(null=True, blank=True)
    b02_mineral = models.FloatField(null=True, blank=True)
    b03_main_metal = models.FloatField(null=True, blank=True)
    b04_other_metal = models.FloatField(null=True, blank=True)  
    b05_petrol = models.FloatField(null=True, blank=True)
    b06_wood = models.FloatField(null=True, blank=True)
    b07_electricity = models.FloatField(null=True, blank=True)
    b08_computer = models.FloatField(null=True, blank=True)
    b09_ufe = models.FloatField(null=True, blank=True)
    b10_machinety = models.FloatField(null=True, blank=True)
    r_usd_try = models.FloatField(null=True, blank=True)
    r_eur_try = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['ac_month']
        db_table = 't_indexes_base'

    def __str__(self):
        return str(self.ac_month)
    


class IndexIncRates(Common):

    rep_month = models.ForeignKey(RepMonth, on_delete=models.PROTECT, verbose_name='Reporting Month')
    ac_month = models.DateField(null=True, blank=True)
    art_ufe = models.FloatField(null=True, blank=True)
    art_tufe = models.FloatField(null=True, blank=True)
    art_usd_try = models.FloatField(null=True, blank=True)
    art_eur_try = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['ac_month']
        db_table = 't_indexes_inc_rates'
        unique_together = ['ac_month','rep_month']

    def __str__(self):
        return self.rep_month.rep_month + str(self.ac_month)