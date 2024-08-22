from django.db import models


class UserWater(models.Model):
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    profile_image=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    lat=models.CharField(max_length=100)
    lng=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    role_id=models.CharField(max_length=10)
    aadhaar_number=models.CharField(max_length=12)
    is_aadhar_verified=models.BooleanField(default=False)
    status=models.BooleanField(default=False)
    fcm_token=models.CharField(max_length=100)
    is_deleted=models.BooleanField(default=False)
    deleted_at=models.CharField(max_length=100,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name
    




class ProductWater(models.Model):
    userId = models.ForeignKey(UserWater, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description=models.CharField(max_length=200)
    image=models.ImageField(upload_to='product_images')
    litre=models.CharField(max_length=100)
    price=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class OrderWater(models.Model):
    fromUser = models.ForeignKey(UserWater, on_delete=models.CASCADE,related_name='orders_from_user')
    toUser = models.ForeignKey(UserWater, on_delete=models.CASCADE,related_name='orders_to_user')
    product=models.ForeignKey(ProductWater, on_delete=models.CASCADE)
    status=models.CharField(max_length=100) #1= ordered #2=delivered #3=cancelled
    remarkCustomer=models.CharField(max_length=100,blank=True)
    remarkSeller=models.CharField(max_length=100,blank=True)
    paid=models.BooleanField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name