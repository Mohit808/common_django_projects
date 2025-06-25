from django.db import models


class UserDating(models.Model):
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
    zoodiac_sign=models.TextField()
    work=models.TextField()
    job_title=models.TextField()
    collageUniversity=models.TextField()
    education_level=models.TextField()
    ethnicity=models.TextField()
    home_town=models.TextField()
    language=models.TextField()
    relation_type=models.TextField()
    smoke=models.BooleanField()
    drink=models.BooleanField()
    marijuana=models.BooleanField()
    drugs=models.BooleanField()
    match_note=models.TextField()

    city=models.CharField(max_length=200)
    state=models.CharField(max_length=200)
    country=models.CharField(max_length=200)
    full_address=models.CharField(max_length=200)
    location_lat=models.CharField(max_length=200)
    location_long=models.CharField(max_length=200)

    def __str__(self):
        return self.text

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
    

