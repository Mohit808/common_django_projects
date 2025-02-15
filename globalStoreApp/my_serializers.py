from rest_framework import serializers
from globalStoreApp.models import OtpModel, Seller, Store, MainCategory, Category,Product,Brand,Tags,Variant, FeatureListModel, OrderItem, Order,Address,Customer, Banner, FestivalOffer, DeliveryPartner,Wallet, Transaction
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
    

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = "__all__"
    


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = "__all__"



class StoreSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        # fields = "__all__"
        fields = ["id","store_name","store_story","store_logo"]

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
    # brand = BrandSerializer(read_only=True)
    discount_percentage = serializers.SerializerMethodField()
    main_category_name=serializers.CharField(source='main_category.name', read_only=True) 
    category_name=serializers.CharField(source='category.name', read_only=True) 
    variant_name=serializers.CharField(source='variant.name', read_only=True) 
    brand_name=serializers.CharField(source='brand.name', read_only=True) 
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


class DeliveryPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryPartner
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



class CreateOrderSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.store_name', read_only=True)
    store_logo = serializers.CharField(source='store.store_logo', read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.store_name', read_only=True)
    store_logo = serializers.SerializerMethodField()
    store_address = serializers.CharField(source='store.store_address', read_only=True)
    store_building = serializers.CharField(source='store.store_building', read_only=True)
    store_floor = serializers.CharField(source='store.store_floor', read_only=True)
    store_tower = serializers.CharField(source='store.store_tower', read_only=True)
    store_landmark = serializers.CharField(source='store.store_landmark', read_only=True)
    pincode = serializers.CharField(source='store.pincode', read_only=True)
    store_how_to_reach = serializers.CharField(source='store.store_how_to_reach', read_only=True)
    store_country = serializers.CharField(source='store.store_country', read_only=True)
    store_state = serializers.CharField(source='store.store_state', read_only=True)
    store_city = serializers.CharField(source='store.store_city', read_only=True)
    store_lat = serializers.CharField(source='store.lat', read_only=True)
    store_lng = serializers.CharField(source='store.lng', read_only=True)
    orderItem= OrderItemSerializer(many=True,required=False)
    deliveryPartner = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def get_deliveryPartner(self, obj):
        if obj.deliveryPartner:
            return {
                'id': obj.deliveryPartner.id,
                'name': obj.deliveryPartner.name,
                'image_url': self.get_deliveryPartner_image(obj.deliveryPartner),
                'bike':obj.deliveryPartner.bike,
                'phone_number': obj.deliveryPartner.phone_number
            }
        return None
    
    def get_customer(self, obj):
        if obj.customer:
            return {
                'id': obj.customer.id,
                'customer_name': obj.customer.name,
                # 'customer_image':obj.customer.image.url,
                'customer_image': self.get_customer_image(obj.customer),
                'mobile':obj.customer.mobile,
                'email': obj.customer.email
            }
        return None
    
    def get_store_logo(self, obj):
        request = self.context.get('request')
        if obj.store and obj.store.store_logo:
            return request.build_absolute_uri(obj.store.store_logo.url) if request else f'{settings.MEDIA_URL}{obj.store.store_logo.url}'
        return None
    
    def get_deliveryPartner_image(self, deliveryPartner):
        request = self.context.get('request')
        if deliveryPartner.image:
            return request.build_absolute_uri(deliveryPartner.image.url) if request else f'{settings.MEDIA_URL}{deliveryPartner.image.url}'
        return None
    
    def get_customer_image(self, customer):
        request = self.context.get('request')
        if customer.image:
            return request.build_absolute_uri(customer.image.url) if request else f'{settings.MEDIA_URL}{customer.image.url}'
        return None

class DeliveryOderSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.store_name', read_only=True)
    store_logo = serializers.CharField(source='store.store_logo', read_only=True)
    store_address = serializers.CharField(source='store.store_address', read_only=True)
    store_lat = serializers.CharField(source='store.lat', read_only=True)
    store_lng = serializers.CharField(source='store.lng', read_only=True)
    customerName = serializers.CharField(source='customer.name', read_only=True)
    customerImage = serializers.CharField(source='customer.image', read_only=True)
    customerMobile = serializers.CharField(source='customer.mobile', read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('otp', None)
        return representation

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = "__all__"


class BannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = "__all__"
    


class FestivalOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = FestivalOffer
        fields = "__all__"
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request is not None:
            representation['image'] = request.build_absolute_uri(instance.image.url)
        return representation


class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = "__all__"

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = "__all__"