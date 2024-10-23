from django.db import models
from common.models import Common
from libraries.models import L4Code
from constants.models import RepMonth
from libraries.models import ActivityTypeDetailIncome
# Create your models here.

   

class IncomeQuantity(Common):
    
    rep_month = models.ForeignKey(RepMonth, on_delete=models.PROTECT, verbose_name='income_rep_month')
    l4_code = models.ForeignKey(L4Code, on_delete=models.PROTECT, verbose_name='income_l4_code')
    inc_month = models.DateField()
    inc_qty = models.FloatField(default=0)
    activity_detail = models.ForeignKey(ActivityTypeDetailIncome, on_delete=models.PROTECT, verbose_name='Income Type Detail',null=True, blank=True)


    class Meta:
        ordering = ['l4_code']
        db_table = 't_inc_qty'

    def __str__(self):
        return self.rep_month.rep_month & "-" & self.l4_code.code_comb
    
class IncomeQuantitybyPPR(Common):
    
    rep_month = models.ForeignKey(RepMonth, on_delete=models.PROTECT, verbose_name='income_rep_month')
    l4_code = models.ForeignKey(L4Code, on_delete=models.PROTECT, verbose_name='income_l4_code')
    inc_month = models.DateField()
    inc_qty = models.FloatField(default=0)
    activity_detail = models.ForeignKey(ActivityTypeDetailIncome, on_delete=models.PROTECT, verbose_name='Income Type Detail',null=True, blank=True)
    ppr_no  = models.IntegerField(default=0)

    class Meta:
        ordering = ['l4_code']
        db_table = 't_inc_qty_ppr'
        unique_together = ('rep_month','l4_code','inc_month','ppr_no', 'activity_detail')

    def __str__(self):
        return self.rep_month.rep_month & "-" & self.l4_code.code_comb
    

class IncomeIndexes(Common):
    inc_month = models.DateField()
    inc_index = models.FloatField(default=0)
    inc_inc_w_otv = models.FloatField(default=0)
    ppr_no  = models.IntegerField(default=0)
    class Meta:
        ordering = ['inc_month']
        db_table = 't_inc_index'
        unique_together = ('inc_month','ppr_no')

    def __str__(self):
        return str(self.inc_month) & "-" & str(self.ppr_no)