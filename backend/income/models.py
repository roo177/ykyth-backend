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