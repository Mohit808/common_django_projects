import random
import string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from globalStoreApp.models import OtpModel
from globalStoreApp.my_serializers import PhoneLoginSerializer, SellerSerializer, CustomerSerializer, DeliveryPartnerSerializer
from globalStoreApp.custom_response import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from globalStoreApp.models import Customer, DeliveryPartner, Seller


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



class SignUpEmailView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        firstName = request.data.get('firstName')
        lastName = request.data.get('lastName')
        
        if email is None:
            return customResponse(message= 'email required', status=status.HTTP_400_BAD_REQUEST)
        if password is None:
            return customResponse(message= 'Password required', status=status.HTTP_400_BAD_REQUEST)
        if firstName is None:
            return customResponse(message= 'firstName required', status=status.HTTP_400_BAD_REQUEST)
        if lastName is None:
            return customResponse(message= 'lastName required', status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user,created=User.objects.get_or_create(username=email,password=password,first_name=firstName,last_name=lastName,email=email)
            token, created=Token.objects.get_or_create(user=user)
            if created:
                serializer=CustomerSerializer(context={'request': request},data={"id":user.id,"email":email,"name":f"{firstName} {lastName}"},partial=True)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return customResponse(message=f"{serializer.errors}",status=status.HTTP_400_BAD_REQUEST)
                queryset =Customer.objects.get(email=email)
                serializer = CustomerSerializer(queryset)
                return customResponse(message= 'Signin successfully', status=status.HTTP_200_OK,data={"token":token.key,"user": serializer.data})
            return customResponse(message="User already exists!",status=400)
                
            # if created:
            #     updateToSeller(user)
            #     return customResponse(message= 'OTP verified successfully', status=status.HTTP_200_OK,data={"token":token.key})
            # return customResponse(message= 'Invalid OTP', status=status.HTTP_200_OK,)
        
        except OtpModel.DoesNotExist:
            return customResponse(message= 'Somthing went wrong', status=status.HTTP_400_BAD_REQUEST)
        



class LoginEmailView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
    
        
        if email is None:
            return customResponse(message= 'email required', status=status.HTTP_400_BAD_REQUEST)
        if password is None:
            return customResponse(message= 'Password required', status=status.HTTP_400_BAD_REQUEST)
    
        
        try:
            user=User.objects.get(username=email,password=password,)

            token, created=Token.objects.get_or_create(user=user)
            queryset =Customer.objects.get(email=email)
            serializer = CustomerSerializer(queryset,context={'request': request})

            print(user.id)
            try:
                querysetDelivery =DeliveryPartner.objects.get(id=user.id)
                serializerDelivery = DeliveryPartnerSerializer(querysetDelivery,context={'request': request})
                delivery_data = serializerDelivery.data

            except DeliveryPartner.DoesNotExist:
                delivery_data = None

            try:
                querysetSeller =Seller.objects.get(id=user.id)
                serializerSeller = SellerSerializer(querysetSeller,context={'request': request})
                seller_data = serializerSeller.data
            except Seller.DoesNotExist:
                seller_data = None 

            return customResponse(message= 'Signin successfully', status=status.HTTP_200_OK,data={"token":token.key,"user": serializer.data,"deliveryPartner":delivery_data,"seller":seller_data})
        
        except User.DoesNotExist:
            return customResponse(message='Invalid credentials', status=status.HTTP_401_UNAUTHORIZED)


# @api_view(['POST',"PUT"])
# def createUser(request):
#     user,created = User.objects.get_or_create(username=request.data.get('userId'))
#     token,created  = Token.objects.get_or_create(user=user)
#     userSer=UsersAllSerializers(data=request.data)
#     if userSer.is_valid():
#         userSer.save()
#         data=userSer.data
#         data['token']=token.key
#         return JsonResponse(data,safe=False)
#     else:
#         return JsonResponse(userSer.errors,safe=False)