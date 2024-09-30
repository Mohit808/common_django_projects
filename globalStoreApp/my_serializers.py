from rest_framework import serializers
from globalStoreApp.models import OtpModel, Seller, Store, MainCategory, Category,Product,Brand,Tags,Variant, FeatureListModel, OrderItem, Order,Address,Customer
from django.conf import settings

class AbsoluteImageField(serializers.ImageField):
    def to_representation(self, value):
        request = self.context.get('request')
        if request is None:
            return super().to_representation(value)
        if value:
            return request.build_absolute_uri(value.url)
        return None
    


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
    


    
class CategorySerializer(serializers.ModelSerializer):
    # image =AbsoluteImageField()
    class Meta:
        model = Category
        fields = "__all__"
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request is not None:
            representation['image'] = request.build_absolute_uri(instance.image.url)
        return representation

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request is not None:
            representation['image'] = request.build_absolute_uri(instance.image.url)
        return representation
    

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = "__all__"
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request is not None:
            representation['image'] = request.build_absolute_uri(instance.image.url)
        return representation
    
        
class MainCategorySerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
   
    class Meta:
        model = MainCategory
        fields = "__all__"

    def get_image(self, obj):
        request = self.context.get('request')
        if request is not None and obj.image and obj.image.url:
            return request.build_absolute_uri(obj.image.url)
        return None 



class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    discount_percentage = serializers.SerializerMethodField()
    store_name = serializers.CharField(source='store.store_name', read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request is not None:
            representation['image'] = request.build_absolute_uri(instance.image.url)
        return representation
    
    def get_discount_percentage(self, obj):
        if obj.price and obj.discountedPrice:
            return (obj.price - obj.discountedPrice) / obj.price * 100
        return 0
    





class FeaturedSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeatureListModel
        fields = "__all__"


    
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    discounted_price = serializers.CharField(source='product.discountedPrice', read_only=True)
    price = serializers.CharField(source='product.price', read_only=True)
    product_image = serializers.SerializerMethodField() 
    class Meta:
        model = OrderItem
        fields = "__all__"
    
    def get_product_image(self, obj):
        request = self.context.get('request')
        if obj.product.image:
            return request.build_absolute_uri(obj.product.image.url) if request else f'{settings.MEDIA_URL}{obj.product.image.url}'
        return None


class OrderSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.store_name', read_only=True)
    store_logo = serializers.CharField(source='store.store_logo', read_only=True)
    # orderItem = serializers.PrimaryKeyRelatedField(many=True,queryset=OrderItem.objects.all())
    # orderItem= OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"
    

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = "__all__"
    










    