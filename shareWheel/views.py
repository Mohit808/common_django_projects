from django.shortcuts import render
from rest_framework.views import APIView
from shareWheel.serializers import *
from shareWheel.models import *
from common_function.custom_response import *

class WheelBookingFunction(APIView):
    def get(self, request,pk=None):
        
        query=WheelBooking.objects.all()

        serializer = WheelBookingSerializer(query, many=True,context={'request': request})
        return customResponse(message= f'Fetch data successfully', status=200  ,data=serializer.data)
    
    def post(self,request,pk=None):
        serializer = WheelBookingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            customResponse(message='created successfully', status=200)
        else : 
            customResponse(message='Failed to create', status=400, data=serializer.errors)
