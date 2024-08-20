from rest_framework import serializers
from globalStoreApp.models import OtpModel, Seller, Store


class PhoneLoginSerializer(serializers.Serializer):
    
    phone_number = serializers.CharField(max_length=10)
    otp = serializers.CharField(max_length=6)
    
    class Meta:
        model = OtpModel
    
    def create(self, validated_data):
        return OtpModel.objects.create(**validated_data)
    


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = "__all__"

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"

    def create(self, validated_data):
        
        request = self.context.get('request')
        try:
            seller = Seller.objects.get(username=request.user)
        except Seller.DoesNotExist:
            raise serializers.ValidationError("Seller profile does not exist for the current user.")
        
        validated_data['seller_id'] = seller

        store = Store.objects.create(**validated_data)
        return store