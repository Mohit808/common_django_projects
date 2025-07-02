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
from django.utils.timesince import timesince
from django.utils import timezone
import random






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



    





@authentication_classes([DatingTokenAuthentication])
@permission_classes([IsAuthenticated])
class SendMessage(APIView):
    def post(self, request):
        receiver_id = request.data.get('receiver')
        text = request.data.get('text')

        if not receiver_id or not text:
            return customResponse(message="Receiver and text are required", status=400)

        try:
            sender = UserModel.objects.get(user=request.user)
        except UserModel.DoesNotExist:
            return customResponse(message="Your profile not found", status=404)

        try:
            receiver = UserModel.objects.get(id=receiver_id)
        except UserModel.DoesNotExist:
            return customResponse(message="Receiver not found", status=404)

        message = Message.objects.create(sender=sender, receiver=receiver, text=text)
        return customResponse(data=MessageSerializer(message).data, message="Message sent", status=201)
    


@authentication_classes([DatingTokenAuthentication])
@permission_classes([IsAuthenticated])
class GetUserMessages(APIView):
    def get(self, request):
        other_user_id = request.GET.get('user_id')
        if not other_user_id:
            return customResponse(message="User ID is required", status=400)

        try:
            sender = UserModel.objects.get(user=request.user)
        except UserModel.DoesNotExist:
            return customResponse(message="Your profile not found", status=404)

        try:
            receiver = UserModel.objects.get(id=other_user_id)
        except UserModel.DoesNotExist:
            return customResponse(message="Other user not found", status=404)

        # fetch conversation thread
        messages = Message.objects.filter(
            Q(sender=sender, receiver=receiver) |
            Q(sender=receiver, receiver=sender)
        ).order_by('date_sent')

        serialized_messages = MessageSerializer(messages, many=True).data

        return customResponse(data=serialized_messages, message="Conversation fetched successfully", status=200)
    





def format_message_time(date_sent):
    now = timezone.now()
    if date_sent.date() == now.date():
        return "Today"
    elif date_sent.date() == (now - timezone.timedelta(days=1)).date():
        return "Yesterday"
    else:
        return date_sent.strftime("%d/%m/%y")



@authentication_classes([DatingTokenAuthentication])
@permission_classes([IsAuthenticated])
class ChatListView(APIView):
    def get(self, request):
        try:
            current_user = UserModel.objects.get(user=request.user)
        except UserModel.DoesNotExist:
            return customResponse(message="Your profile not found", status=404)

        # Fetch all users current_user has exchanged messages with
        message_partners = Message.objects.filter(
            Q(sender=current_user) | Q(receiver=current_user)
        ).values_list('sender', 'receiver')

        # Flatten and deduplicate partner user IDs excluding self
        partner_ids = set()
        for sender_id, receiver_id in message_partners:
            if sender_id and sender_id != current_user.id:
                partner_ids.add(sender_id)
            if receiver_id and receiver_id != current_user.id:
                partner_ids.add(receiver_id)

        chat_list = []

        for partner_id in partner_ids:
            try:
                partner = UserModel.objects.get(id=partner_id)
            except UserModel.DoesNotExist:
                continue

            # Get last message with this partner
            last_message = Message.objects.filter(
                Q(sender=current_user, receiver=partner) | Q(sender=partner, receiver=current_user)
            ).order_by('-date_sent').first()

            if not last_message:
                continue

            # last_message_time = timesince(last_message.date_sent)
            last_message_time = format_message_time(last_message.date_sent)

            is_by_you = last_message.sender == current_user

            unread_count = Message.objects.filter(
                sender=partner, receiver=current_user, is_read=False
            ).count()

            chat_list.append({
                "user_id": partner.id,
                "name": partner.name,
                "profile_picture": partner.profile_picture if partner.profile_picture else "",
                "last_message": last_message.text,
                "last_message_time": last_message_time,
                "unread_count": unread_count,
                "last_message_by_you": is_by_you
            })

        # Sort by latest message
        chat_list = sorted(chat_list, key=lambda x: x['last_message_time'])

        return customResponse(data=chat_list, message="Chat list fetched successfully", status=200)
    



@authentication_classes([DatingTokenAuthentication])
@permission_classes([IsAuthenticated])
class StandoutView(APIView):
    def post(self, request):
        data = request.data.copy()
        data['user_standout'] = request.user.id
        
        serializer = StandoutSerializer(data=data)
        if serializer.is_valid():
            standout = serializer.save()
            return customResponse(data=StandoutSerializer(standout).data, message="Standout created successfully", status=201)

        return customResponse(message=serializer.errors, status=400)
    
    def get(self, request):
        try:
            current_user = UserModel.objects.get(user=request.user)
            standout = Standout.objects.exclude(user_standout=current_user)
            standout = standout.order_by('-priority')
            if not standout:
                return customResponse(message="No standout found for this user", status=404)
            
            paginator = PageNumberPagination()
            paginator.page_size = 10
            paginated_standout = paginator.paginate_queryset(standout, request) 
            data = StandoutSerializer(paginated_standout, many=True).data
            return customResponse(data=data, message="Standout fetched successfully", status=200)
        except Standout.DoesNotExist:
            return customResponse(message="Standout not found", status=404)


@authentication_classes([DatingTokenAuthentication])
@permission_classes([IsAuthenticated])
class SponsoredView(APIView):
    def post(self, request):
        data = request.data.copy()
        data['sender'] = request.user.id
        try:
            receiver = UserModel.objects.get(id=data['receiver'])
            data['receiver'] = receiver.user.id
        except UserModel.DoesNotExist:
            return customResponse(message="Receiver not found", status=404)
        
        if data['sender'] == data['receiver']:
            return customResponse(message="You cannot send a sponsored outing to yourself", status=400)
        
        #outing_status should not pending
        if SponsoredOuting.objects.filter(sender_id=data['sender'], receiver_id=data['receiver'],outing_status__in=['pending', 'accepted']).exists():
            return customResponse(message="You have already sent a sponsored outing to this user", status=400)

        data['outing_status'] = 'pending'
        otp = str(random.randint(100000, 999999))
        data['otp'] = otp

        

        try:
            sender = UserModel.objects.get(user=request.user)
        except UserModel.DoesNotExist:
            return customResponse(message="Your profile not found", status=404)
        
        data['sender'] = sender.id

        serializer = SponsoredOutingSerializerPost(data=data)
        if serializer.is_valid():
            outing = serializer.save()
            return customResponse(data=SponsoredOutingSerializerPost(outing).data, message="Sponsored outing created successfully", status=201)

        return customResponse(message=serializer.errors, status=400)
    
    def get(self, request):
        try:
            sent = request.GET.get('sent')
            current_user = UserModel.objects.get(user=request.user)
            if sent:
                outings = SponsoredOuting.objects.filter(sender=current_user)
            else:
                outings = SponsoredOuting.objects.filter(receiver=current_user)
            if not outings:
                return customResponse(message="No sponsored outings found for this user", status=404)
            
            paginator = PageNumberPagination()
            paginator.page_size = 10
            paginated_outings = paginator.paginate_queryset(outings, request) 
            data = SponsoredOutingSerializer(paginated_outings, many=True).data
            return customResponse(data=data, message="Sponsored outings fetched successfully", status=200)
        except SponsoredOuting.DoesNotExist:
            return customResponse(message="Sponsored outing not found", status=404)
        
    def put(self, request):
        data = request.data.copy()
        outing_id = data.get('outing_id')
        if not outing_id:
            return customResponse(message="Outing ID is required", status=400)
        
        status = data.get('status')
        if status not in ['accepted', 'rejected', 'completed']:
            return customResponse(message="Invalid status", status=400)
        

        data['outing_status'] = status

        try:
            outing = SponsoredOuting.objects.get(id=outing_id)
        except SponsoredOuting.DoesNotExist:
            return customResponse(message="Sponsored outing not found", status=404)
        
        if status == 'rejected':
            outing.delete()
            return customResponse(message="Sponsored outing rejected successfully", status=200)

        serializer = SponsoredOutingSerializer(outing, data=data, partial=True)
        if serializer.is_valid():
            updated_outing = serializer.save()
            return customResponse(data=SponsoredOutingSerializer(updated_outing).data, message="Sponsored outing updated successfully", status=200)

        return customResponse(message=serializer.errors, status=400)



@authentication_classes([DatingTokenAuthentication])
@permission_classes([IsAuthenticated])
class SponsoredList(APIView):
    def get(self, request):
        
        current_lat =request.query_params.get('latitude')
        current_lon = request.query_params.get('longitude')
        if current_lat or current_lon:
            user_model = UserModel.objects.exclude(user=request.user).annotate(
                distance=ExpressionWrapper(
                    (Abs(F('location_lat') - float(current_lat)) + Abs(F('location_long') - float(current_lon))),
                    output_field=FloatField())).order_by('distance')
        else:
            user_model = UserModel.objects.exclude(user=request.user)

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_user_model = paginator.paginate_queryset(user_model, request)
        serialized_users = UserSerializer(paginated_user_model, many=True).data
        return customResponse(data=serialized_users, message="Sponsored users fetched successfully", status=200)



@authentication_classes([DatingTokenAuthentication])
@permission_classes([IsAuthenticated])
class GiftView(APIView):
    def post(self, request):
        data = request.data.copy()
        data['url'] = data.get('url', '').strip()
        
        serializer = GiftSerializer(data=data)
        if serializer.is_valid():
            gift = serializer.save()
            return customResponse(data=GiftSerializer(gift).data, message="Gift created successfully", status=201)

        return customResponse(message=serializer.errors, status=400)
    
    def get(self, request):
        gifts = Gift.objects.all()
        if not gifts:
            return customResponse(message="No gifts found", status=404)
        
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_gifts = paginator.paginate_queryset(gifts, request) 
        data = GiftSerializer(paginated_gifts, many=True).data
        return customResponse(data=data, message="Gifts fetched successfully", status=200)
    


@authentication_classes([DatingTokenAuthentication])
@permission_classes([IsAuthenticated])
class MyGiftView(APIView):
    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id

        gift_map = request.data.get('gifts')
        if not gift_map or not isinstance(gift_map, dict):
            return customResponse(message="Gifts dictionary is required", status=400)

        created_gifts = []

        for gift_id, quantity in gift_map.items():
            try:
                gift = Gift.objects.get(id=gift_id)
            except Gift.DoesNotExist:
                return customResponse(message=f"Gift with id {gift_id} not found", status=404)
            
            single_data = {
                    'user': request.user.id,
                    'gift': gift.id,
                    'quantity': quantity
                }
            serializer = MyGiftSerializer(data=single_data)
            if serializer.is_valid():
                my_gift = serializer.save()
                created_gifts.append(MyGiftSerializer(my_gift).data)
            else:
                return customResponse(message=serializer.errors, status=400)
                

        return customResponse(data=created_gifts, message="Gifts sent successfully", status=201)
    
    def get(self, request):
        try:
            my_gifts = MyGift.objects.filter(user=request.user.id)
            if not my_gifts:
                return customResponse(message="No gifts found for this user", status=404)
            
            paginator = PageNumberPagination()
            paginator.page_size = 10
            paginated_my_gifts = paginator.paginate_queryset(my_gifts, request) 
            data = MyGiftSerializer2(paginated_my_gifts, many=True).data
            return customResponse(data=data, message="My gifts fetched successfully", status=200)
        except MyGift.DoesNotExist:
            return customResponse(message="My gifts not found", status=404)



@authentication_classes([DatingTokenAuthentication])
@permission_classes([IsAuthenticated])
class GiftToSend(APIView):
    def get(self, request):
        try:
        
            my_gifts = MyGift.objects.filter(user=request.user.id)
            my_gifts_gift_ids = my_gifts.values_list('gift', flat=True)
            gifts = Gift.objects.exclude(id__in=my_gifts_gift_ids)

            # Combine both lists into one
            all_gifts = list(my_gifts) + list(gifts)

            # Paginate the combined list
            paginator = PageNumberPagination()
            paginator.page_size = 10
            paginated_all_gifts = paginator.paginate_queryset(all_gifts, request)

            # Serialize: use MyGiftSerializer2 for MyGift instances, GiftSerializer for Gift instances
            data = []
            for item in paginated_all_gifts:
                if isinstance(item, MyGift):
                    data.append(MyGiftSerializer2(item).data)
                else:
                    data.append(GiftSerializer(item).data)

            if not data:
                return customResponse(message="No gifts found", status=404)

            return customResponse(
                data=data,
                message="Gifts to send fetched successfully",
                status=200
            )
        except Gift.DoesNotExist:
            return customResponse(message="Gifts not found", status=404)