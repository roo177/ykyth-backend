from django.db import models
from common.models import Common
from constants.models import Unit, RepMonth


class M1Code(Common):

    m1_code = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    code_comb = models.CharField(max_length=255, editable=True, blank=True)
    
    class Meta:
        ordering = ['m1_code']
        db_table = 't_m1_code'
        unique_together = ['code_comb']

    def save(self, *args, **kwargs):
        if self.m1_code:
            self.code_comb = f"{self.m1_code}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code_comb
    
class M2Code(Common):

    m2_code = models.CharField(max_length=100)
    m1_code = models.ForeignKey(M1Code, on_delete=models.PROTECT, verbose_name='Y1 Code')
    description = models.CharField(max_length=100)
    code_comb = models.CharField(max_length=255, editable=True, blank=True)
    
    class Meta:
        ordering = ['m2_code']
        db_table = 't_m2_code'
        unique_together = ['code_comb']

    def save(self, *args, **kwargs):
        if self.m1_code:
            self.code_comb = f"{self.m1_code.m1_code}-{self.m2_code}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code_comb
    
class T1Code(Common):
    PRICE_ADJUSTMENT_TYPES = [
        ('FFK AK', 'FFK AK'),
        ('YKT AK', 'YKT AK'),
        ('BKM AK', 'BKM AK'),
        ('EUR AK', 'EUR AK'),
        ('USD AK', 'USD AK'),
        ('DGS.01', 'DGS.01'),
        ('DGS.02', 'DGS.02'),
        ('PTS.01', 'PTS.01'),
        ('PTS.02', 'PTS.02'),
        ('RYS.01', 'RYS.01'),
        ('RYS.02', 'RYS.02'),
        ('RYS.03', 'RYS.03'),
        ('OZD.01', 'OZD.01'),
        ('OZD.02', 'OZD.02'),
        ('-', '-'),
        ('GFF AK', 'GFF AK'),
    ]  

    t1_code = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    code_comb = models.CharField(max_length=255, editable=True, blank=True)
    price_adjustment = models.CharField(max_length=100, choices=PRICE_ADJUSTMENT_TYPES, null=True, blank=True)
    contract_no = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        ordering =['t1_code','price_adjustment']
        db_table = 't_t1_code'
        unique_together = ['t1_code','price_adjustment']


    def save(self, *args, **kwargs):
        if self.t1_code:
            self.code_comb = f"{self.t1_code}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code_comb
    
# Create your models here.
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
class L1Code(Common):

    l1_code = models.CharField(max_length=1)
    description = models.CharField(max_length=100)
    code_comb = models.CharField(max_length=255, editable=True, blank=True)
    
    class Meta:
        ordering = ['l1_code']
        db_table = 't_l1_code'
        unique_together = ['code_comb']

    def save(self, *args, **kwargs):
        if self.l1_code:
            self.code_comb = f"{self.l1_code}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code_comb
    
class L2Code(Common):
    
    l2_code = models.CharField(max_length=6)
    l1_code = models.ForeignKey(L1Code, on_delete=models.PROTECT, verbose_name='L1 Code')
    description = models.CharField(max_length=100)
    code_comb = models.CharField(max_length=255, editable=True, blank=True)
    
    class Meta:
        ordering = ['l2_code']
        db_table = 't_l2_code'
        unique_together = ['code_comb']

    def save(self, *args, **kwargs):
        if self.l1_code:
            self.code_comb = f"{self.l1_code.l1_code}-{self.l2_code}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code_comb
    
class L3Code(Common):
        
        l3_code = models.CharField(max_length=6)
        l2_code = models.ForeignKey(L2Code, on_delete=models.PROTECT, verbose_name='L2 Code')
        description = models.CharField(max_length=100)
        code_comb = models.CharField(max_length=255, editable=True, blank=True)
        
        class Meta:
            ordering = ['l3_code']
            db_table = 't_l3_code'
            unique_together = ['code_comb']

        def save(self, *args, **kwargs):
            if self.l2_code:
                self.code_comb = f"{self.l2_code.l1_code.l1_code}-{self.l2_code.l2_code}-{self.l3_code}"
            super().save(*args, **kwargs)

        def __str__(self):
            return self.code_comb


class L4Code(Common):
        
        l4_code = models.CharField(max_length=3)
        l3_code = models.ForeignKey(L3Code, on_delete=models.PROTECT, verbose_name='L3 Code')
        description = models.CharField(max_length=255)
        unit = models.ForeignKey(Unit, null=True, on_delete=models.PROTECT, verbose_name='Unit')
        mtc_dgs_nkt = models.CharField(max_length=10,null=True, blank=True)
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
        code_comb = models.CharField(max_length=255, editable=True, blank=True)
        activity_type = models.ForeignKey(ActivityType, on_delete=models.PROTECT, verbose_name='Income Activity Type',null=True, blank=True)
        activity_detail = models.ForeignKey(ActivityTypeDetail, on_delete=models.PROTECT, verbose_name='Income Activity Type Detail',null=True, blank=True)
        l4_order_ratio = models.FloatField(null=True, blank=True)
        l4_delivery_ratio = models.FloatField(null=True, blank=True)
        l4_handover_ratio = models.FloatField(null=True, blank=True)

        def save(self, *args,
                 
                  **kwargs):
            if self.l3_code:
                self.code_comb = f"{self.l3_code.l2_code.l1_code.l1_code}-{self.l3_code.l2_code.l2_code}-{self.l3_code.l3_code}-{self.l4_code}"
            super().save(*args, **kwargs)

        def __str__(self):
            return self.code_comb + " / " + self.description[:25]

        class Meta:
            ordering = ['code_comb']
            db_table = 't_l4_code'
            unique_together = ['aygm_code', 'activity_type','activity_detail','code_comb']

class R1Code(Common):

    r1_code = models.CharField(max_length=5)
    description = models.CharField(max_length=100)
    code_comb = models.CharField(max_length=255, editable=True, blank=True)
    
    class Meta:
        ordering = ['code_comb']
        db_table = 't_r1_code'
        unique_together = ['code_comb']

    def save(self, *args, **kwargs):
        if self.r1_code:
            self.code_comb = f"{self.r1_code}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code_comb
    
class R2Code(Common):
    
    r2_code = models.CharField(max_length=4)
    r1_code = models.ForeignKey(R1Code, on_delete=models.PROTECT, verbose_name='R1 Code')
    description = models.CharField(max_length=100)
    code_comb = models.CharField(max_length=255, editable=True, blank=True)
    
    class Meta:
        ordering = ['code_comb']
        db_table = 't_r2_code'
        unique_together = ['code_comb']
    def save(self, *args, **kwargs):
        if self.r1_code:
            self.code_comb = f"{self.r1_code.r1_code}-{self.r2_code}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code_comb
    
class R3Code(Common):
        
        r3_code = models.CharField(max_length=4)
        r2_code = models.ForeignKey(R2Code, on_delete=models.CASCADE, verbose_name='R2 Code')
        description = models.CharField(max_length=100)
        code_comb = models.CharField(max_length=255, editable=True, blank=True)
        
        class Meta:
            ordering = ['code_comb']
            db_table = 't_r3_code'
            unique_together = ['code_comb']
        def save(self, *args, **kwargs):
            if self.r2_code:
                self.code_comb = f"{self.r2_code.r1_code.r1_code}-{self.r2_code.r2_code}-{self.r3_code}"
            super().save(*args, **kwargs)

        def __str__(self):
            return self.code_comb


class R4Code(Common):

        r4_code = models.CharField(max_length=4)
        r3_code = models.ForeignKey(R3Code, on_delete=models.CASCADE, verbose_name='R3 Code')
        description = models.CharField(max_length=255)
        code_comb = models.CharField(max_length=255, editable=True, blank=True)
        machine_id = models.CharField(max_length=100, null=True, blank=True)


        def save(self, *args, **kwargs):
            if self.r3_code:
                self.code_comb = f"{self.r3_code.r2_code.r1_code.r1_code}-{self.r3_code.r2_code.r2_code}-{self.r3_code.r3_code}-{self.r4_code}"
            super().save(*args, **kwargs)

        def __str__(self):
            return self.code_comb + " / " + self.description

        class Meta:
            ordering = ['code_comb']
            db_table = 't_r4_code'
            unique_together = ['code_comb']

