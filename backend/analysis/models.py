from django.db import models
from common.models import Common
# Create your models here.

class Analysis(Common):
    
    l4_ = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    
    class Meta:
        ordering = ['key']
        db_table = 't_analysis'


    def __str__(self):
        return self.key