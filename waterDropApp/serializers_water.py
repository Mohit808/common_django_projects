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


class OrderWaterSerializerForSave(serializers.ModelSerializer):
    class Meta:
        model = OrderWater
        fields = '__all__' 



class OrderWaterSerializer(serializers.ModelSerializer):
    fromUser = serializers.SerializerMethodField()
    toUser = serializers.SerializerMethodField()
    product = ProductWaterSerializer()
    class Meta:
        model = OrderWater
        fields = '__all__' 
    
    def get_fromUser(self, obj):
        """
        Conditionally include 'fromUser' details in the serialized data.
        """
        if self.context.get('include_fromUser', True) and obj.fromUser:
            return UserWaterSerializer(obj.fromUser).data
        return None

    def get_toUser(self, obj):
        """
        Conditionally include 'toUser' details in the serialized data.
        """
        if self.context.get('include_toUser', True) and obj.toUser:
            return UserWaterSerializer(obj.toUser).data
        return None

    def to_representation(self, instance):
        """
        Custom representation of the model instance.
        """
        representation = super().to_representation(instance)
        # Remove fields if the condition is not met
        if not self.context.get('include_fromUser', True):
            representation.pop('fromUser', None)
        if not self.context.get('include_toUser', True):
            representation.pop('toUser', None)
        return representation