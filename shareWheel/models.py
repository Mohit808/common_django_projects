from django.db import models


class WheelBooking(models.Model):
    customer=models.SmallIntegerField()
    addressFrom=models.CharField(max_length=200)
    latitudeFrom=models.FloatField()
    longitudeFrom=models.FloatField()
    addressTo=models.CharField(max_length=200)
    latitudeTo=models.FloatField()
    longitudeTo=models.FloatField()
    vehicle=models.CharField(max_length=20)
    driver=models.SmallIntegerField()
    status=models.CharField(max_length=20)
    polylineRide=models.TextField()
    polylineDriver=models.TextField()