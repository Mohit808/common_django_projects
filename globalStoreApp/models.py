from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import RegexValidator




class OtpModel(models.Model):
    phone_number = models.CharField(max_length=10)
    otp = models.CharField(max_length=6)

    def __str__(self):
        return self.phone_number
    


class Customer(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=50)
    image=models.ImageField(blank=True)
    mobile=models.CharField(max_length=20,blank=True)
    email=models.CharField(max_length=50,blank=True)
    
    def __str__(self) :
        return self.name
    
    class Meta:
        db_table = "globalStoreApp_customer"


class Address(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    address_type=models.CharField(max_length=10)
    full_address=models.CharField(max_length=200)
    house_no=models.CharField(max_length=100,blank=True)
    area=models.CharField(max_length=100,blank=True)
    landmark=models.CharField(max_length=100,blank=True)
    instruction=models.CharField(max_length=200,blank=True)
    latitude=models.FloatField()
    longitude=models.FloatField()

    def __str__(self) :
        return self.full_address



class Seller(models.Model):
    id=models.IntegerField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100,unique=True)
    phone_number = models.CharField(max_length=20)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    whatsapp_number=models.CharField(max_length=20)
    profile_image=models.CharField(max_length=100)
    role_id=models.CharField(max_length=10)
    social_login_type=models.CharField(max_length=10)
    social_login_id=models.CharField(max_length=100)
    is_phone_number_verified=models.BooleanField(default=False)
    is_email_verified=models.BooleanField(default=False)
    aadhaar_number=models.CharField(max_length=12)
    aadhaar_front=models.ImageField(blank=True)
    aadhaar_back=models.ImageField(blank=True)
    is_aadhar_verified=models.BooleanField(default=False)
    status=models.BooleanField(default=False)
    fcm_token=models.CharField(max_length=100)
    is_deleted=models.BooleanField(default=False)
    deleted_at=models.CharField(max_length=100,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.username}{self.id}"

    

class Store(models.Model):
    id=models.IntegerField(primary_key=True)
    # seller_id=models.ForeignKey(Seller,on_delete=models.CASCADE)
    store_name= models.CharField(max_length=100)
    store_slug= models.SlugField(max_length=100)
    business_owner_name= models.CharField(max_length=100)
    store_mobile=models.CharField(max_length=20,blank=True)
    store_email=models.CharField(max_length=100,blank=True)

    store_logo= models.ImageField()
    store_banner= models.ImageField()
    store_story= models.CharField(max_length=100)
    store_type= models.CharField(max_length=100)
    gst_number= models.CharField(max_length=12,blank=True)
    pan_number= models.CharField(max_length=10,blank=True)
    store_description= models.CharField(max_length=100)
    service_type=models.CharField(max_length=10)
    categories= models.CharField(max_length=100)
    store_code= models.CharField(max_length=100)
    store_code_text= models.CharField(max_length=100)
    loyalty_points= models.CharField(max_length=10)

    # address_title=models.CharField(max_length=100,blank=True)
    # full_address=models.CharField(max_length=200,blank=True)
    # house_no=models.CharField(max_length=100,blank=True)
    # area=models.CharField(max_length=100,blank=True)
    # landmark=models.CharField(max_length=100,blank=True)
    # instruction=models.CharField(max_length=200,blank=True)
    # latitude=models.FloatField(default=0)
    # longitude=models.FloatField(default=0)

    store_address= models.CharField(max_length=100)
    store_building= models.CharField(max_length=100,blank=True)
    store_floor= models.CharField(max_length=100,blank=True)
    store_tower= models.CharField(max_length=100,blank=True)
    store_landmark= models.CharField(max_length=100,blank=True)
    pincode= models.CharField(max_length=10)
    store_how_to_reach= models.CharField(max_length=100,blank=True)
    store_country= models.CharField(max_length=100)
    store_state= models.CharField(max_length=100)
    store_city= models.CharField(max_length=100)
    lat= models.CharField(max_length=10)
    lng= models.CharField(max_length=10)
    subscription_plan_id= models.CharField(max_length=10)
    store_visibility= models.CharField(max_length=10)
    store_status= models.CharField(max_length=10)
    store_privacy_policy= models.CharField(max_length=100)
    store_tnc= models.CharField(max_length=100)
    store_refund_policy= models.CharField(max_length=100)
    is_pickup= models.BooleanField(default=False)
    is_deleted= models.BooleanField(default=False)
    def __str__(self):
        return f"{self.id} : {self.store_name}"



class MainCategory(models.Model):
    name = models.CharField(max_length=100)
    image =  models.ImageField(upload_to="product_images",blank=True,)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "MainCategory"
        verbose_name_plural = "MainCategories"

class Category(models.Model):
    main_category = models.ForeignKey(MainCategory, blank=True, null=True, on_delete=models.SET_NULL,related_name='categories')
    name = models.CharField(max_length=100)
    image =  models.ImageField(upload_to="product_images")
    description = models.TextField()
    def __str__(self):
        return f"{self.id} {self.name}"
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Variant(models.Model):
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)
    image =  models.ImageField(upload_to="product_images")
    description = models.TextField()
    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)
    image =  models.ImageField(upload_to="product_images")
    description = models.TextField()
    def __str__(self):
        return self.name

class Tags(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Product(models.Model):
    name= models.CharField(max_length=100)
    description=models.TextField()
    highlight=models.TextField(blank=True)
    image= models.ImageField(upload_to="product_images")
    imageMain= models.TextField(blank=True)
    images=models.TextField(blank=True)
    price= models.FloatField()
    discountedPrice= models.FloatField(null=True,blank=True)
    unit= models.CharField(max_length=100,null=True)
    qty= models.SmallIntegerField(null=True,blank=True)
    stock= models.SmallIntegerField(null=True, blank=True)
    store= models.ForeignKey(Store,on_delete=models.CASCADE,null=True, blank=True)
    main_category= models.ForeignKey(MainCategory,on_delete=models.CASCADE,null=True, blank=True)
    category= models.ForeignKey(Category,on_delete=models.CASCADE)
    variant= models.ForeignKey(Variant,on_delete=models.CASCADE,null=True, blank=True)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE, null=True, blank= True)
    tag =models.ManyToManyField(Tags, blank= True)
    origin=models.TextField(blank= True)
    tips= models.TextField(blank= True)
    additional_info = models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class FeatureListModel(models.Model):
    name= models.CharField(max_length=100)
    highlight=models.TextField(blank=True)
    image= models.ImageField(upload_to="product_images",blank=True)
    main_category= models.ForeignKey(MainCategory,on_delete=models.CASCADE,null=True, blank=True)
    category= models.ForeignKey(Category,on_delete=models.CASCADE)
    variant= models.ForeignKey(Variant,on_delete=models.CASCADE,null=True, blank=True)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE, null=True, blank= True)
    priority= models.IntegerField(default=0,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Priority {self.priority} : {self.name}"

class DeliveryPartner(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=100)
    image=models.ImageField()
    phone_number=models.CharField(max_length=20,null=True,blank=True)
    email=models.CharField(max_length=100,blank=True)
    aadhaar=models.BigIntegerField(null=True,blank=True,validators=[RegexValidator(r'^\d{12}$', 'Aadhaar number must be 12 digits.')])
    bike=models.CharField(max_length=20,blank=True)
    address=models.CharField(max_length=200)
    latitude=models.FloatField(default=0)
    longitude=models.FloatField(default=0)


    def __str__(self):
        return f"{self.name}"


class OrderItem(models.Model):
    product= models.ForeignKey(Product,on_delete=models.CASCADE)
    qty=models.PositiveSmallIntegerField(default=1)
    store=models.ForeignKey(Store,on_delete=models.CASCADE)
    price= models.FloatField(null=True,blank=True)
    discountedPrice= models.FloatField(null=True,blank=True)

    def __str__(self):
        return f"{self.product.name} (x{self.qty})"
    

# totalAmount=0
        # discountedAmount=0
class Order(models.Model):
    store= models.ForeignKey(Store,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    deliveryPartner=models.ForeignKey(DeliveryPartner,on_delete=models.SET_NULL,null=True,blank=True)
    orderItem= models.ManyToManyField(OrderItem) 
    totalAmount=models.FloatField(null=True,blank=True)
    discountedTotalAmount=models.FloatField(null=True,blank=True)
    otp=models.CharField(blank=True,max_length=10)
    status=models.IntegerField(blank=True,default=0)
    statusName=models.CharField(blank=True,max_length=100)
    cancelReason=models.CharField(blank=True,max_length=100)
    tip=models.FloatField(blank=True,max_length=9,default=0)
    address_type=models.CharField(max_length=10,blank=True)
    address_title=models.CharField(max_length=100,blank=True)
    full_address=models.CharField(max_length=200,blank=True)
    house_no=models.CharField(max_length=100,blank=True)
    area=models.CharField(max_length=100,blank=True)
    landmark=models.CharField(max_length=100,blank=True)
    instruction=models.CharField(max_length=200,blank=True)
    latitude=models.FloatField(default=0)
    longitude=models.FloatField(default=0)
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} : {self.store.store_name}"


    # def __str__(self):
        # product_names = ", ".join([product.name for product in self.product.all()])
        # return f"{self.store.store_name[:15]} : {product_names}"


class Banner(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    description=models.CharField(max_length=200)
    buttonText=models.CharField(max_length=200,)
    image=models.ImageField()
    store=models.ForeignKey(Store,null=True,on_delete=models.CASCADE)
    priority=models.SmallIntegerField(default=0)
    startColor=models.CharField(max_length=10,null=True)
    endColor=models.CharField(max_length=100,null=True)

    def __str__(self) :
        return self.name
    

class FestivalOffer(models.Model):
    variant=models.ManyToManyField(Variant)
    name=models.CharField(max_length=200)
    description=models.CharField(max_length=200)
    image=models.ImageField()
    priority=models.SmallIntegerField()

    def __str__(self) :
        return self.name
    

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        (0, 'Credit'),
        (1, 'Debit'),
        (2, 'withdraw request'),
    ]
    orderId=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    amount=models.FloatField()
    type=models.IntegerField(choices=TRANSACTION_TYPE_CHOICES) # //0= credit or 1=debit, 2=withdraw request
    remark=models.CharField(max_length=200)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self) :
        return f"{self.amount}"
    
class Wallet(models.Model):
    balance=models.FloatField(default=0)
    pending_amount=models.FloatField(default=0)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self) :
        return f"{self.customer.id} : {self.customer.name} , Balance : {self.balance} , Pending : {self.pending_amount}"

class WithdrawRequest(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    amount=models.FloatField()

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self) :
        return f"{self.customer.id} : {self.customer.name} , Amount : {self.amount}"


class Notification(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    heading=models.CharField(max_length=100)
    description=models.TextField(blank=True)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self) :
        return f"{self.balance}"
    


class Story(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    image=models.ImageField()
    description=models.TextField(blank=True)
    latitude=models.FloatField(default=0)
    longitude=models.FloatField(default=0)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self) :
        return f"{self.balance}"
    

