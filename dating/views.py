from django.shortcuts import render
from common_function.custom_response import *
from rest_framework.views import APIView
from dating.models import *
from dating.serializers import *
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from .authentication import DatingTokenAuthentication




def hello(request):
    return customResponse(status=200,message="Successfull")

class Hello(APIView):
    def get(self, request,pk=None):
       return customResponse(data="Hello",message= f'Fetch data successfully', status=200)
    





class DatingRegisterView(APIView):
    def post(self, request):
        data = request.data.copy()
        data['email'] = data.get('email', '').strip().lower()
        data['username'] = data.get('email', '')
        serializer = DatingUserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            token = DatingToken.objects.create(user=user)
            
            return Response({
                'message': 'Login successful',
                'token': token.key,
                'user': {'id': user.id, 'email': user.email}},status=200)

            # return Response({
            #     'id': user.id,
            #     'email': user.email,
            #     'token': token.key
            # }, status=status.HTTP_201_CREATED)
        
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class DatingLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        email = email.strip().lower() if email else None
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=400)

        try:
            user = DatingUser.objects.get(email=email)
        except DatingUser.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=401)

        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=401)

        token, created = DatingToken.objects.get_or_create(user=user)

        return Response({
            'message': 'Login successful',
            'token': token.key,
            'user': {'id': user.id, 'email': user.email}
        }, status=200)
    




@authentication_classes([DatingTokenAuthentication])
@permission_classes([IsAuthenticated])
class Onboarding(APIView):
    def post(self,request):
        data=request.data.copy()
        data['_id']=request.user.id
        serializer = UserSerializer(data=data,partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return customResponse(message="data saved successfully", status=200)
        return customResponse(message=f"{serializer.errors}",status=400)






@authentication_classes([DatingTokenAuthentication])
@permission_classes([IsAuthenticated])
class Home(APIView):
    def post(self,request):
    
        return customResponse(data="Logged in successfully",message="Logged in successfully",status=200)

