import random
import string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from globalStoreApp.models import OtpModel
from globalStoreApp.my_serializers import PhoneLoginSerializer, SellerSerializer
from globalStoreApp.custom_response import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token




# mobile number already exists then replace it with new otp

class LoginView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        if phone_number is not None:
            otp = generate_otp()

            existing_user = OtpModel.objects.filter(phone_number=phone_number).first()
            if existing_user:
                existing_user.otp = otp
                existing_user.save()
                return customResponse(message= 'OTP sent successfully', status=status.HTTP_200_OK)

            serializer = PhoneLoginSerializer(data={"phone_number": phone_number, "otp": otp})
            if serializer.is_valid():
                serializer.save()
                return customResponse(message='OTP sent successfully', status=status.HTTP_200_OK)
        return customResponse(message="phone number required", status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        user_otp = request.data.get('otp')
        
        if phone_number is None:
            return customResponse(message= 'phone number required', status=status.HTTP_400_BAD_REQUEST)
        if user_otp is None:
            return customResponse(message= 'OTP required', status=status.HTTP_400_BAD_REQUEST)
        
        try:
            appUser = OtpModel.objects.get(phone_number=phone_number)
            if appUser.otp==user_otp:
                user,created=User.objects.get_or_create(username=phone_number)
                token, created=Token.objects.get_or_create(user=user)
                
                if created:
                    updateToSeller(user)

                return customResponse(message= 'OTP verified successfully', status=status.HTTP_200_OK,data={"token":token.key})
            return customResponse(message= 'Invalid OTP', status=status.HTTP_200_OK,)
        
        except OtpModel.DoesNotExist:
            return customResponse(message= 'Invalid phone number', status=status.HTTP_400_BAD_REQUEST)
           

def generate_otp():
    value= ''.join(random.choices(string.digits, k=6))
    return value


def updateToSeller(user):
    ser=SellerSerializer(data={"username": user.username}, partial=True)
    if ser.is_valid():
        ser.save()
    return customResponse(message= 'User updated successfully', status=status.HTTP_200_OK)