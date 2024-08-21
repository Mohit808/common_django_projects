from rest_framework import serializers, status
from rest_framework.response import Response
from .models import UserWater, ProductWater

class UserWaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWater
        fields = '__all__' 


class ProductWaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductWater
        fields = '__all__' 
