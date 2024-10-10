from rest_framework import serializers
from shareWheel.models import WheelBooking
from django.conf import settings

class WheelBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = WheelBooking
        fields = "__all__"  