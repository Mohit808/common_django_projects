from django.shortcuts import render
from rest_framework.views import APIView
from shareWheel.serializers import *
from shareWheel.models import *
from common_function.custom_response import *

class WheelBooking(APIView):
    def get(self, request,pk=None):
        
        query=WheelBooking.objects.all()

        serializer = WheelBookingSerializer(query, many=True,context={'request': request})
        return customResponse(message= f'Fetch data successfully', status=200  ,data=serializer.data)
    
