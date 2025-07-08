from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
import binascii
import os


class DatingUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class DatingUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50)
    birth_date = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='datinguser_set',   # 👈 unique related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='datinguser_set',   # 👈 unique related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    objects = DatingUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    


class DatingToken(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    user = models.OneToOneField(DatingUser, related_name='auth_token', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()
    
    
class UserModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(DatingUser, on_delete=models.CASCADE,default=None)
    username=models.CharField(max_length=100,blank=True)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    gender=models.CharField(max_length=10)
    marital_status=models.CharField(max_length=10)
    birth_date=models.CharField(max_length=10)
    bio=models.CharField(max_length=200)
    likes=models.CharField(max_length=500,null=True)
    profile_picture=models.CharField(max_length=200)
    images=models.CharField(max_length=1000,null=True)
    height=models.CharField(max_length=200)
    weight=models.CharField(max_length=200)
    question1=models.TextField()
    answer1=models.TextField()
    question2=models.TextField()
    answer2=models.TextField()
    video=models.TextField()
    video_promt=models.TextField()
    zodiac_sign=models.CharField(max_length=100)
    work=models.CharField(max_length=100)
    job_title=models.CharField(max_length=100)
    collageUniversity=models.CharField(max_length=200)
    education_level=models.CharField(max_length=100)
    ethnicity=models.CharField(max_length=100)
    home_town=models.CharField(max_length=100)
    language=models.CharField(max_length=200)
    relation_type=models.CharField(max_length=100)
    smoke=models.CharField(max_length=10, null=True)
    drink=models.CharField(max_length=10, null=True)
    marijuana=models.CharField(max_length=10, null=True)
    drugs=models.CharField(max_length=10, null=True)
    match_note=models.TextField()

    city=models.CharField(max_length=200)
    state=models.CharField(max_length=200)
    country=models.CharField(max_length=200)
    full_address=models.CharField(max_length=200)
    location_lat=models.CharField(max_length=200)
    location_long=models.CharField(max_length=200)

    def __str__(self):
        return f"{self.id}"+" : "+f"{self.name}"

class UserPreference(models.Model):
    text=models.TextField()
    image=models.TextField(null=True,blank=True)

    def __str__(self):
        return self.text

class Photo(models.Model):
    text=models.TextField()
    image=models.TextField(null=True,blank=True)

    def __str__(self):
        return self.text

class LikeDating(models.Model):
    sender=models.ForeignKey(UserModel, related_name='likes_sent', on_delete=models.CASCADE, null=True)
    receiver=models.ForeignKey(UserModel, related_name='likes_received', on_delete=models.CASCADE, null=True)
    message=models.TextField(null=True, blank=True)
    gift=models.ForeignKey('Gift', on_delete=models.CASCADE, null=True, blank=True)
    date=models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.id}" +" : "+ self.sender.name + " likes " + self.receiver.name


class Match(models.Model):
    sender=models.ForeignKey(UserModel,related_name='matches_sent', on_delete=models.CASCADE, null=True)
    receiver=models.ForeignKey(UserModel,related_name='matches_received',on_delete=models.CASCADE, null=True)
    date=models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.sender.name + " matched with " + self.receiver.name

class Message(models.Model):
    sender = models.ForeignKey(UserModel, related_name='messages_sent', on_delete=models.CASCADE,null=True)
    receiver = models.ForeignKey(UserModel, related_name='messages_received', on_delete=models.CASCADE,null=True)
    text = models.TextField(null=True)
    date_sent = models.DateTimeField(auto_now_add=True, null=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.name} → {self.receiver.name}: {self.text[:30]}"

class Report(models.Model):
    text=models.TextField()
    image=models.TextField(null=True,blank=True)

    def __str__(self):
        return self.text

class Block(models.Model):
    text=models.TextField()
    image=models.TextField(null=True,blank=True)

    def __str__(self):
        return self.text

class Subscription(models.Model):
    text=models.TextField()
    image=models.TextField(null=True,blank=True)

    def __str__(self):
        return self.text

class DatingNotification(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True)
    message = models.TextField(null=True)

    def __str__(self):
        return self.text

class Device(models.Model):
    text=models.TextField()
    image=models.TextField(null=True,blank=True)

    def __str__(self):
        return self.text



class Standout(models.Model):
    user_standout = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return self.user_standout.name + " - Priority: " + str(self.priority)
    

class SponsoredOuting(models.Model):
    sender = models.ForeignKey(UserModel,related_name="sender_sponsored", on_delete=models.CASCADE, null=True)
    receiver = models.ForeignKey(UserModel,related_name="receiver_sponsored", on_delete=models.CASCADE, null=True)
    outing_type = models.CharField(max_length=100, null=True)
    outing_date = models.DateTimeField(null=True)
    from_time = models.CharField(max_length=20, null=True)
    to_time = models.CharField(max_length=20, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    location = models.CharField(max_length=200, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    avenue_name=models.CharField(max_length=200, null=True)
    outing_status = models.CharField(max_length=50, null=True)
    description = models.TextField(null=True, blank=True)
    payment_status = models.CharField(max_length=20,null=True)
    otp= models.CharField(max_length=6, null=True)

    def __str__(self):
        return f"{self.sender.name} - Outing on {self.outing_date.strftime('%Y-%m-%d')}" if self.outing_date else f"{self.sender.name} - Outing"
    

class Gift(models.Model):
    url= models.URLField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f"Gift URL: {self.url}" if self.url else "Gift without URL"


class MyGift(models.Model):
    quantity = models.IntegerField(default=1)
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.name} - (x{self.quantity})" if self.gift else f"{self.user.name} - Gift without URL"
    


class Support(models.Model):
    sender = models.ForeignKey(UserModel,related_name="sender_support", on_delete=models.CASCADE, null=True)
    message = models.TextField(null=True)

    def __str__(self):
        return f"{self.sender.name} - Support Message" if self.sender else "Support Message without Sender"



class AiMatch(models.Model):
    user1 = models.ForeignKey(UserModel,related_name="user1", on_delete=models.CASCADE, null=True)
    user2 = models.ForeignKey(UserModel,related_name="user2",on_delete=models.CASCADE, null=True)
    message= models.TextField(null=True, blank=True)

    def __str__(self):
        return f"AI Match between {self.user1.name} and {self.user2.name}" if self.user1 and self.user2 else "AI Match without Users"
