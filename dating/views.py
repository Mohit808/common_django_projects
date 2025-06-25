from django.shortcuts import render
from common_function.custom_response import *
from rest_framework.views import APIView
from dating.models import *
from dating.serializers import *
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User



def hello(request):
    return customResponse(status=200,message="Successfull")

class Hello(APIView):
    def get(self, request,pk=None):
       return customResponse(data="Hello",message= f'Fetch data successfully', status=200)
    





class DatingRegisterView(APIView):
    def post(self, request):
        data = request.data.copy()
        data['username'] = data.get('email', '')
        serializer = DatingUserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            token = DatingToken.objects.create(user=user)
            return Response({
                'id': user.id,
                'email': user.email,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    def post(self,request):
    
        return customResponse(data="Logged in successfully",message="Logged in successfully",status=200)

