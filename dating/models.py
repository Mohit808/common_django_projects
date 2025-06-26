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
    profile_picture=models.CharField(max_length=200)
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

class Like(models.Model):
    text=models.TextField()
    image=models.TextField(null=True,blank=True)

    def __str__(self):
        return self.text


class Match(models.Model):
    text=models.TextField()
    image=models.TextField(null=True,blank=True)

    def __str__(self):
        return self.text

class Message(models.Model):
    text=models.TextField()
    image=models.TextField(null=True,blank=True)

    def __str__(self):
        return self.text

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

class Notification(models.Model):
    text=models.TextField()
    image=models.TextField(null=True,blank=True)

    def __str__(self):
        return self.text

class Device(models.Model):
    text=models.TextField()
    image=models.TextField(null=True,blank=True)

    def __str__(self):
        return self.text
    

