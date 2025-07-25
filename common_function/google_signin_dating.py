from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth.models import User
from globalStoreApp.custom_response import customResponse
from django.core.exceptions import ObjectDoesNotExist
from dating.serializers import *
from dating.models import *


class DatingGoogleLoginView(APIView):
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

            # dating user create
            data = {
                'email': email,
                'username': email,
            }
        
            serializer = DatingUserSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()
                token,created = DatingToken.objects.get_or_create(user=user)            
                try:
                    user = DatingUser.objects.get(email=email)
                    user_model = UserModel.objects.get(user=user)
                except DatingUser.DoesNotExist:
                    return customResponse(message="Email does not exists", status=404)
                except UserModel.DoesNotExist:
                    user_model = None 
                
                return customResponse(message= 'Signin successfully', status=status.HTTP_200_OK,data={"token":token.key,"user": UserSerializer(user_model).data})
            

        except ValueError:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
