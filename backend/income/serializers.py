

from rest_framework import serializers
from .models import IncomeQuantity

class IncomeQuantitySerializer(serializers.ModelSerializer):

    class Meta:
        model = IncomeQuantity
        fields = '__all__'

        