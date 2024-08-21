import random
import string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from waterDropApp.serializers_water import UserWaterSerializer
from globalStoreApp.models import OtpModel
from globalStoreApp.custom_response import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from waterDropApp.models import UserWater


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        id_token = request.data.get('id_token')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        profile_image = request.data.get('profile_image')


        if email is None:
            return customResponse(message= 'email required', status=status.HTTP_400_BAD_REQUEST)
        if id_token is None:
            return customResponse(message= 'Id Token required', status=status.HTTP_400_BAD_REQUEST)
        
        user,created=User.objects.get_or_create(username=email,password=id_token,first_name=first_name,last_name=last_name,email=email)
        token, created=Token.objects.get_or_create(user=user)

        if created:
            updateDatabase(request,email,first_name,last_name,profile_image)
        queryset =UserWater.objects.get(email=email)
        serializer = UserWaterSerializer(queryset)
        return customResponse(message= 'Signin successfully', status=status.HTTP_200_OK,data={"token":token.key,"user": serializer.data})
    

def updateDatabase(request,email,first_name,last_name,profile_image):
    print(email,first_name,last_name,profile_image)
    ser=UserWaterSerializer(data={"email":email,"first_name":first_name,"last_name":last_name,"profile_image":profile_image},context={'request': request}, partial=True)
    if ser.is_valid():
        ser.save()
    print(ser.data)
    return customResponse(message= 'User updated successfully', status=status.HTTP_200_OK)







class UpdateUser(APIView):
    def post(self, request):
        user_instance = UserWater.objects.get(id=request.data.get('id'))
        serializer = UserWaterSerializer(user_instance,data=request.data,context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return customResponse(message= 'User updated successfully', status=status.HTTP_200_OK)
        return customResponse(message= 'Invalid data', status=400  ,data=serializer.data)



