from django.db import models
from common.models import Common
# Create your models here.

class Constant(Common):
    
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    
    class Meta:
        ordering = ['key']
        db_table = 't_constant'


    def __str__(self):
        return self.key
    
class RepMonth(Common):

    rep_month = models.CharField(max_length=100)
    month = models.IntegerField()
    year = models.IntegerField()
    rep_month_date = models.DateField()

    
    class Meta:
        ordering = ['rep_month_date']
        db_table = 't_rep_month'

        
    def __str__(self):
        return self.rep_month
    
class Unit(Common):

    unit = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['unit']
        db_table = 't_unit'

        
    def __str__(self):
        return self.unit