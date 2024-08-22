from rest_framework import serializers, status
from rest_framework.response import Response
from .models import UserWater, ProductWater, OrderWater

class UserWaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWater
        fields = '__all__' 


class ProductWaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductWater
        fields = '__all__' 

class OrderWaterSerializer(serializers.ModelSerializer):
    fromUser = UserWaterSerializer()
    toUser = UserWaterSerializer()
    class Meta:
        model = OrderWater
        fields = '__all__' 
    
    def get_fromUser(self, obj):
        # Example condition to check if 'fromUser' details should be included
        if self.context.get('include_fromUser', True):
            return UserWaterSerializer(obj.fromUser).data
        return None

    def get_toUser(self, obj):
        # Example condition to check if 'toUser' details should be included
        if self.context.get('include_toUser', True):
            return UserWaterSerializer(obj.toUser).data
        return None
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not self.context.get('include_fromUser', True):
            representation.pop('fromUser', None)
        if not self.context.get('include_toUser', True):
            representation.pop('toUser', None)
        return representation
