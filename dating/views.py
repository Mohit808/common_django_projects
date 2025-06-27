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
            user_model = UserModel.objects.get(user=user)
        except DatingUser.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=401)
        except UserModel.DoesNotExist:
            user_model = None 

        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=401)

        token, created = DatingToken.objects.get_or_create(user=user)

        return Response({
            'message': 'Login successful',
            'token': token.key,
            # 'user': {'id': user.id, 'email': user.email},
            'user':UserSerializer(user_model).data if user_model else None 
        }, status=200)
    




@authentication_classes([DatingTokenAuthentication])
@permission_classes([IsAuthenticated])
class Onboarding(APIView):
    def post(self,request):
        data=request.data.copy()
        try:
            profile = UserModel.objects.get(user=request.user)
            serializer = UserSerializer(profile, data=data, partial=True)
        except UserModel.DoesNotExist:
            data['user'] = request.user.id
            serializer = UserSerializer(data=data,partial=True)

        if serializer.is_valid():
            user_model=serializer.save()
            return customResponse(data=UserSerializer(user_model).data,message="Data saved successfully", status=200)

        return customResponse(message=f"{serializer.errors}", status=400)
    
        # data['id']=request.user.id
        # serializer = UserSerializer(data=data,partial=True)
        # if serializer.is_valid():
        #     user = serializer.save()
        #     return customResponse(message="data saved successfully", status=200)
        # return customResponse(message=f"{serializer.errors}",status=400)






@authentication_classes([DatingTokenAuthentication])
@permission_classes([IsAuthenticated])
class Home(APIView):
    def get(self,request):
        user_model = UserModel.objects.all()
        # user_model = UserModel.objects.exclude(user=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_user_model = paginator.paginate_queryset(user_model, request)
        return customResponse(data=paginated_user_model,message="Logged in successfully",status=200)

