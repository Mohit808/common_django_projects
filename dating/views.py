from django.shortcuts import render
from common_function.custom_response import *
from rest_framework.views import APIView
from dating.models import *
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User


def hello(request):
    return customResponse(status=200,message="Successfull")

class Hello(APIView):
    def get(self, request,pk=None):
       return customResponse(data="Hello",message= f'Fetch data successfully', status=200)
    

class Login(APIView):
    def post(self,request):
    
        return customResponse(data="Logged in successfully",message="Logged in successfully",status=200)

