from django.db import models
from common.models import Common
from constants.models import Unit, RepMonth
from libraries.models import R4Code, L4Code, M2Code, T1Code,R3Code

class R4Price(Common):
    PRICE_ADJUSTMENT_TYPES = [
        ('FFK AK', 'FFK AK'),
        ('YKT AK', 'YKT AK'),
        ('BKM AK', 'BKM AK'),
        ('EUR AK', 'EUR AK'),
        ('USD AK', 'USD AK'),
        ('-', '-'),
    ]
    FIN_TYPE_CHOICES = [
        ('Sell & LB', 'Sell & LB'),
        ('Leasing', 'Leasing'),
        ('Nakit', 'Nakit'),
    ]
    CURRENCY_CHOICES = [
        ('EUR', 'EUR'),
        ('USD', 'USD'),
        ('TRY', 'TRY'),
    ]
    ORIGIN_CHOICES = [
        ('TR', 'TR'),
        ('OECD', 'OECD'),
        ('OEKB', 'OEKB'),
        ('SACE', 'SACE'),
        ('UKEF', 'UKEF'),
        ('KUKE', 'KUKE'),
        ('-', '-'),
    ]
    DEPRECIATION_TYPES = [
        ('MAKİNE', 'MAKİNE'),
        ('SABİT TESİS', 'SABİT TESİS'),
        ('ARAÇ', 'ARAÇ'),
        ('DİĞER EKİPMANLAR', 'DİĞER EKİPMANLAR'),
        ('-', '-'),
    ]
    ENERGY_TYPES = [
        ('ELEKTRİK', 'ELEKTRİK'),
        ('DOĞALGAZ', 'DOĞALGAZ'),
        ('BUHAR', 'BUHAR'),
        ('MAZOT', 'MAZOT'),
        ('-', '-'),
    ]
    rep_month = models.ForeignKey(RepMonth, on_delete=models.PROTECT, verbose_name='Reporting Month')
    r4_code = models.ForeignKey(R4Code, on_delete=models.CASCADE, verbose_name='R4 Code', related_name='r4_prices')
    unit = models.ForeignKey(Unit, null=True, on_delete=models.PROTECT, verbose_name='Unit',related_name='unit_r4_prices')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, null=True, blank=True)
    origin = models.CharField(max_length=100, choices=ORIGIN_CHOICES, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    price_date = models.DateField(null=True, blank=True)
    price_adjustment_type = models.CharField(max_length=100, choices=PRICE_ADJUSTMENT_TYPES,null=True, blank=True )
    bool_depreciation = models.BooleanField(default=False)
    depreciation_type = models.CharField(max_length=100, choices=DEPRECIATION_TYPES,null=True, blank=True )
    depreciation_price = models.FloatField(null=True, blank=True)
    energy_type = models.CharField(max_length=100, choices=ENERGY_TYPES,null=True, blank=True )
    operator_r4_code = models.ForeignKey(R4Code, on_delete=models.CASCADE, verbose_name='Operator R4 Code', null=True, blank=True, related_name='operator_r4_prices')
    operator_m2_code = models.ForeignKey(M2Code, on_delete=models.PROTECT, verbose_name='Operator M2 Code', null=True, blank=True, related_name='operator_m2_prices')
    operator_t1_code = models.ForeignKey(T1Code, on_delete=models.PROTECT, verbose_name='Operator T1 Code', null=True, blank=True, related_name='operator_t1_prices')
    fin_type = models.CharField(max_length=100, choices=FIN_TYPE_CHOICES, null=True, blank=True)
    customs = models.BooleanField(default=False)
    content_constant = models.FloatField(null=True, blank=True)
    machine_id = models.CharField(max_length=100, null=True, blank=True)
    depreciation_quantity = models.FloatField(null=True, blank=True)
    energy_consumption = models.FloatField(null=True, blank=True)
    energy_unit = models.ForeignKey(Unit, null=True, on_delete=models.PROTECT, verbose_name='Energy Unit name', blank=True, related_name='energy_unit_r4_prices')   
    capacity = models.FloatField(null=True, blank=True)
    capacity_unit = models.ForeignKey(Unit, null=True, on_delete=models.PROTECT, verbose_name='Capacity Unit name', blank=True, related_name='capacity_unit_r4_prices')
    m2_code = models.ForeignKey(M2Code, on_delete=models.PROTECT, verbose_name='M2 Code',null=True, blank=True)
    t1_code = models.ForeignKey(T1Code, on_delete=models.PROTECT, verbose_name='T1 Code',null=True, blank=True)

    class Meta:
        ordering = ['price_date']
        db_table = 't_r4_price'
        unique_together = ['r4_code', 'rep_month', 'm2_code', 't1_code', 'price_adjustment_type']

    def __str__(self):
        return str(self.rep_month) + ' - ' + self.r4_code.code_comb
    


class ExpenseAnalysis(Common):

    rep_month = models.ForeignKey(RepMonth, on_delete=models.PROTECT, verbose_name='Reporting Month Analysis')
    l4_code =models.ForeignKey(L4Code, on_delete=models.PROTECT, verbose_name='L4 Code Analysis', related_name='l4_code_analysis')
    r4_code = models.ForeignKey(R4Code, on_delete=models.PROTECT, verbose_name='R4 Code Analysis', related_name='r4_prices_analysis',null=True, blank=True)
    r4_desc = models.CharField(max_length=100, null=True, blank=True)
    work_ratio = models.FloatField(null=True, blank=True)
    work_ratio_desc = models.CharField(max_length=100, null=True, blank=True)
    output_per_unit_time = models.FloatField(null=True, blank=True)
    output_desc = models.CharField(max_length=100, null=True, blank=True)
    consumption_per_unit_time = models.FloatField(null=True, blank=True)
    consumption_desc = models.CharField(max_length=100, null=True, blank=True)
    m2_code = models.ForeignKey(M2Code, on_delete=models.PROTECT, verbose_name='M2 Code', related_name='m2_code_analysis',null=True, blank=True)
    t1_code = models.ForeignKey(T1Code, on_delete=models.PROTECT, verbose_name='T1 Code', related_name='t1_code_analysis',null=True, blank=True)
    r3_code_machine = models.ForeignKey(R3Code, on_delete=models.PROTECT, verbose_name='R3 Code Machine', related_name='r3_code_machine',null=True, blank=True)
    r3_currency = models.CharField(max_length=3, choices=R4Price.CURRENCY_CHOICES, null=True, blank=True)

    class Meta:
        ordering = ['rep_month', 'r4_code__code_comb']
        db_table = 't_exp_analysis'


    def __str__(self):
        return str(self.rep_month) + ' - ' + self.r4_code.code_comb
    


class ExpenseQuantity(Common):
    
    rep_month = models.ForeignKey(RepMonth, on_delete=models.PROTECT, verbose_name='Expense_rep_month')
    l4_code = models.ForeignKey(L4Code, on_delete=models.PROTECT, verbose_name='Expense_l4_code')
    exp_month = models.DateField()
    exp_qty = models.FloatField(default=0)
    m2_code = models.ForeignKey(M2Code, on_delete=models.PROTECT, verbose_name='M2 Code', related_name='m2_code_expense_qty')
    t1_code = models.ForeignKey(T1Code, on_delete=models.PROTECT, verbose_name='T1 Code', related_name='t1_code_expense_qty')

    class Meta:
        ordering = ['l4_code']
        db_table = 't_exp_qty'

    def __str__(self):
        return self.rep_month.rep_month & "-" & self.l4_code.code_comb
    
class ExpenseMachineryOperatorDistribution(Common):
    rep_month = models.ForeignKey(RepMonth, on_delete=models.PROTECT, verbose_name='Expense_rep_month')
    l4_code = models.ForeignKey(L4Code, on_delete=models.PROTECT, verbose_name='Expense_l4_code')
    r4_code = models.ForeignKey(R4Code, on_delete=models.PROTECT, verbose_name='Expense_r4_code')
    machine_r4_code = models.ForeignKey(R4Code, on_delete=models.PROTECT, verbose_name='Machine_r4_code', related_name='machine_r4_code', null=True, blank=True)
    exp_month = models.DateField()  
    machine_qty = models.FloatField(default=0)
    m2_code = models.ForeignKey(M2Code, on_delete=models.PROTECT, verbose_name='M2 Code', related_name='m2_code_expense_machiner',null=True, blank=True)
    t1_code = models.ForeignKey(T1Code, on_delete=models.PROTECT, verbose_name='T1 Code', related_name='t1_code_expense_machiner',null=True, blank=True)
    class Meta:
        ordering = ['l4_code']
        db_table = 't_exp_mach_oper_dist'
        
    def __str__(self):
        return self.rep_month.rep_month & "-" & self.l4_code.code_comb & "-" & self.r4_code.code_comb
    
class Expense(Common):
    CURRENCY = [
        ('TRY', 'TRY'),
        ('EUR', 'EUR'),
        ('USD', 'USD'),
    ]
 
    rep_month = models.ForeignKey(RepMonth, on_delete=models.PROTECT, verbose_name='Expense_rep_month')
    l4_code = models.ForeignKey(L4Code, on_delete=models.PROTECT, verbose_name='Expense_l4_code')
    r3_code = models.ForeignKey(R3Code, on_delete=models.PROTECT, verbose_name='Expense_r3_code',null=True, blank=False)
    r4_code = models.ForeignKey(R4Code, on_delete=models.PROTECT, verbose_name='Expense_r4_code',null=True, blank=False)
    m2_code = models.ForeignKey(M2Code, on_delete=models.PROTECT, verbose_name='M2 Code', related_name='m2_code_expense',null=False, blank=False)
    t1_code = models.ForeignKey(T1Code, on_delete=models.PROTECT, verbose_name='T1 Code', related_name='t1_code_expense',null=False, blank=False)
    exp_month = models.DateField()
    exp_qty = models.FloatField(default=0)
    exp_unit = models.ForeignKey(Unit, on_delete=models.PROTECT, verbose_name='Expense Unit', related_name='exp_unit',null=True, blank=True)
    exp = models.FloatField(default=0)
    currency = models.CharField(max_length=3, choices=CURRENCY, null=True, blank=True)
    bool_depriciation = models.BooleanField(default=False)
 
    class Meta:
        ordering = ['l4_code__code_comb', 'm2_code__code_comb', 't1_code__code_comb','exp_month']
        db_table = 't_exp'
        unique_together = ['rep_month', 'r3_code', 'r4_code', 'm2_code', 't1_code', 'exp_month','currency']

    def __str__(self):
        return self.rep_month.rep_month & "-" & self.l4_code.code_comb & "-" & self.m2_code.code_comb & "-" & self.t1_code.code_comb
 