from rest_framework import serializers, status
from rest_framework.response import Response
from .models import UserWater

class UserWaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWater
        fields = '__all__' 
