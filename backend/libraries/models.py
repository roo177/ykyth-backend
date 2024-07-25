from django.db import models
from common.models import Common
from constants.models import Unit

# Create your models here.

class L1Code(Common):

    l1_code = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    code_comb = models.CharField(max_length=255, editable=False, blank=True)
    
    class Meta:
        ordering = ['l1_code']
        db_table = 't_l1_code'

    def save(self, *args, **kwargs):
        if self.l1_code:
            self.code_comb = f"{self.l1_code}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code_comb
    
class L2Code(Common):
    
    l2_code = models.CharField(max_length=100)
    l1_code = models.ForeignKey(L1Code, on_delete=models.PROTECT, verbose_name='L1 Code')
    description = models.CharField(max_length=100)
    code_comb = models.CharField(max_length=255, editable=False, blank=True)
    
    class Meta:
        ordering = ['l2_code']
        db_table = 't_l2_code'

    def save(self, *args, **kwargs):
        if self.l1_code:
            self.code_comb = f"{self.l1_code.l1_code}-{self.l2_code}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code_comb
    
class L3Code(Common):
        
        l3_code = models.CharField(max_length=100)
        l2_code = models.ForeignKey(L2Code, on_delete=models.PROTECT, verbose_name='L2 Code')
        description = models.CharField(max_length=100)
        code_comb = models.CharField(max_length=255, editable=False, blank=True)
        
        class Meta:
            ordering = ['l3_code']
            db_table = 't_l3_code'

        def save(self, *args, **kwargs):
            if self.l2_code:
                self.code_comb = f"{self.l2_code.l1_code.l1_code}-{self.l2_code.l2_code}-{self.l3_code}"
            super().save(*args, **kwargs)

        def __str__(self):
            return self.code_comb

class ActivityType(Common):
    
    description = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['description']
        db_table = 't_act_type'


    def __str__(self):
        return self.description
    

class ActivityTypeDetail(Common):
    
    description = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['description']
        db_table = 't_act_type_detail'

    def __str__(self):
        return self.description
    
class ActivityTypeDetailIncome(Common):
    
    description = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['description']
        db_table = 't_act_type_detail_inc'

    def __str__(self):
        return self.description
class L4Code(Common):
        
        l4_code = models.CharField(max_length=100)
        l3_code = models.ForeignKey('L3Code', on_delete=models.PROTECT, verbose_name='L3 Code')
        description = models.CharField(max_length=255)
        unit = models.ForeignKey(Unit, null=True, on_delete=models.PROTECT, verbose_name='Unit')
        mtc_dgs_nkt = models.CharField(max_length=10)
        nak_ote = models.IntegerField(null=True, blank=True)
        l4_ref = models.CharField(max_length=100, null=True, blank=True)
        l4_hkds = models.BooleanField(default=False)
        l4_calc_method = models.CharField(max_length=255, null=True, blank=True)
        l4_bf_dg = models.FloatField(null=True, blank=True)
        l4_mk_ks = models.FloatField(null=True, blank=True)
        tax = models.BooleanField(default=False)
        aygm_code = models.CharField(max_length=100, null=True, blank=True)
        aygm_group = models.CharField(max_length=100, null=True, blank=True)
        aygm_desc = models.TextField(null=True, blank=True)
        code_comb = models.CharField(max_length=255, editable=False, blank=True)
        activity_type = models.ForeignKey(ActivityType, on_delete=models.PROTECT, verbose_name='Income Activity Type')
        activity_detail = models.ForeignKey(ActivityTypeDetail, on_delete=models.PROTECT, verbose_name='Income Activity Type Detail')
        l4_order_ratio = models.FloatField(null=True, blank=True)
        l4_delivery_ratio = models.FloatField(null=True, blank=True)
        l4_handover_ratio = models.FloatField(null=True, blank=True)

        def save(self, *args, **kwargs):
            if self.l3_code:
                self.code_comb = f"{self.l3_code.l2_code.l1_code.l1_code}-{self.l3_code.l2_code.l2_code}-{self.l3_code.l3_code}-{self.l4_code}"
            super().save(*args, **kwargs)

        def __str__(self):
            return self.code_comb

        class Meta:
            ordering = ['l4_code']
            db_table = 't_l4_code'
            unique_together = ['aygm_code', 'activity_type','activity_detail','code_comb']

