from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth.models import User
from django.contrib.auth import login

from rest_framework.authtoken.models import Token
from globalStoreApp.my_serializers import CustomerSerializer
from globalStoreApp.custom_response import customResponse
from globalStoreApp.models import Customer

class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get("token")

        if not token:
            return Response({"error": "Token not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verify the token with Google
            print(token)
            try:
                idinfo = id_token.verify_oauth2_token(token, requests.Request())
            except ValueError as e:
                print(f"Token verification failed: {e}")
                return Response({"error": "Invalid token verification"}, status=status.HTTP_400_BAD_REQUEST)

            # idinfo contains: email, sub (user id), picture, name, etc.
            email = idinfo.get("email")
            name = idinfo.get("name")
            picture_url = idinfo.get("picture") 

            print(picture_url)

            print(email, name)

            # Get or create user
            user, created = User.objects.get_or_create(username=email, defaults={"email": email, "first_name": name})

            token, created=Token.objects.get_or_create(user=user)            
            
            # return Response({"message": "Login successful", "email": email}, status=200)
            if created:
                serializer=CustomerSerializer(context={'request': request},data={"id":user.id,"email":email,"name":f"{name}","image":f"{picture_url}"},partial=True)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return customResponse(message=f"{serializer.errors}",status=status.HTTP_400_BAD_REQUEST)
            queryset =Customer.objects.get(email=email)
            if not queryset.image and picture_url:
                queryset.image = picture_url
                queryset.save()
            serializer = CustomerSerializer(queryset)
            return customResponse(message= 'Signin successfully', status=status.HTTP_200_OK,data={"token":token.key,"user": serializer.data})
            

        except ValueError:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
