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
from django.db.models import F, FloatField, ExpressionWrapper
from django.db.models.functions import Abs
from django.db.models import Q




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
        
        current_lat =request.query_params.get('latitude')
        current_lon = request.query_params.get('longitude')
        if current_lat or current_lon:
            user_model = UserModel.objects.exclude(user=request.user).annotate(
                distance=ExpressionWrapper(
                    (Abs(F('location_lat') - float(current_lat)) + Abs(F('location_long') - float(current_lon))),
                    output_field=FloatField())).order_by('distance')
        else:
            user_model = UserModel.objects.all()

        # user_model = UserModel.objects.exclude(user=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_user_model = paginator.paginate_queryset(user_model, request)
        serialized_users = UserSerializer(paginated_user_model, many=True).data

        try:
            current_user_model = UserModel.objects.get(user=request.user)
        except UserModel.DoesNotExist:
            pass

        likes=LikeDating.objects.filter(receiver=current_user_model)
        serialized_like=LikeSerializer(likes, many=True).data

        return Response({
            "message": "Data fetched successfully",
            "status": 200,
            "data": serialized_users,
            "match":serialized_like
        })


# @authentication_classes([DatingTokenAuthentication])
# @permission_classes([IsAuthenticated])
# class Like(APIView):
#     def post(self,request):
#         if not request.data.get('receiver'):
#             return customResponse(message="Receiver is required", status=400)
#         data = request.data.copy()
#         data['sender'] = request.user.id
#         try:
#             receiver = UserModel.objects.get(id=data['receiver'])
#             data['receiver'] = receiver.user.id
#         except UserModel.DoesNotExist:
#             return customResponse(message="Receiver not found", status=404)
        
#         if data['sender'] == data['receiver']:
#             return customResponse(message="You cannot like yourself", status=400)
        
#         if LikeDating.objects.filter(sender_id=data['sender'], receiver_id=data['receiver']).exists():
#             return customResponse(message="You have already liked this user", status=400)

#         serializer = LikeSerializer(data=data)
#         if serializer.is_valid():
#             like = serializer.save()
#             return customResponse(data=LikeSerializer(like).data, message="Like created successfully", status=201)

#         return customResponse(message=f"{serializer.errors}", status=400)



@authentication_classes([DatingTokenAuthentication])
@permission_classes([IsAuthenticated])
class Like(APIView):
    def post(self, request):
        receiver_id = request.data.get('receiver')
        if not receiver_id:
            return customResponse(message="Receiver is required", status=400)

        try:
            sender = UserModel.objects.get(user=request.user)
        except UserModel.DoesNotExist:
            return customResponse(message="Your profile not found", status=404)

        try:
            UserModel.objects.get(id=receiver_id)
        except UserModel.DoesNotExist:
            return customResponse(message="Receiver not found", status=404)

        if sender.id == int(receiver_id):
            return customResponse(message="You cannot like yourself", status=400)

        if LikeDating.objects.filter(sender_id=sender.id, receiver_id=receiver_id).exists():
            return customResponse(message="You have already liked this user", status=400)

        data = {
            'sender': sender.id,
            'receiver': receiver_id
        }

        serializer = LikeRequestSerializer(data=data)
        if serializer.is_valid():
            like = serializer.save()
            return customResponse(data=LikeRequestSerializer(like).data, message="Like created successfully", status=201)

        return customResponse(message=serializer.errors, status=400)
    



@authentication_classes([DatingTokenAuthentication])
@permission_classes([IsAuthenticated])
class AcceptRequest(APIView):
    def post(self,request):
        if not request.data.get('like_id'):
            return customResponse(message="Like ID is required", status=400)
        data = request.data.copy()
        try:
            like = LikeDating.objects.get(id=data['like_id'])
        except LikeDating.DoesNotExist:
            return customResponse(message="Like not found", status=404)

        if Match.objects.filter(sender=like.sender, receiver=like.receiver).exists():
            return customResponse(message="You have already matched with this user", status=400)
        match = Match.objects.create(sender=like.sender, receiver=like.receiver)
        like.delete()
        return customResponse(message="Like accepted successfully", status=200)


@authentication_classes([DatingTokenAuthentication])
@permission_classes([IsAuthenticated])
class RejectRequest(APIView):
    def post(self, request):
        if not request.data.get('like_id'):
            return customResponse(message="Like ID is required", status=400)
        data = request.data.copy()
        try:
            like = LikeDating.objects.get(id=data['like_id'])
        except LikeDating.DoesNotExist:
            return customResponse(message="Like not found", status=404)

        like.delete()
        return customResponse(message="Request rejected successfully", status=200)
    
@authentication_classes([DatingTokenAuthentication])
@permission_classes([IsAuthenticated])
class Matches(APIView):
    def get(self, request):
        try:
            user_model = UserModel.objects.get(user=request.user)
        except UserModel.DoesNotExist:
            return customResponse(message="Your profile not found", status=404)

        matches = Match.objects.filter(sender=user_model.id) | Match.objects.filter(receiver=user_model.id)
        serialized_matches = MatchSerializer(matches, many=True).data

        return customResponse(data=serialized_matches, message="Matches fetched successfully", status=200)

@authentication_classes([DatingTokenAuthentication])
@permission_classes([IsAuthenticated])
class Unmatch(APIView):
    def post(self, request):
        if not request.data.get('user_id'):
            return customResponse(message="User ID is required", status=400)

        try:
            user_model = UserModel.objects.get(user=request.user)
        except UserModel.DoesNotExist:
            return customResponse(message="Your profile not found", status=404)

        other_user_id = request.data.get('user_id')

        match = Match.objects.filter(
            Q(sender=user_model.id, receiver=other_user_id) |
            Q(sender=other_user_id, receiver=user_model.id)
        ).first()

        if not match:
            return customResponse(message="Match not found", status=404)

        match.delete()
        return customResponse(message="Unmatched successfully", status=200)