from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.views import APIView
from globalStoreApp.custom_response import *
# from globalStoreApp.models import *
from globalStoreApp.my_serializers import *
from django.db.models import F, FloatField, ExpressionWrapper
import random
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Value
import requests


@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class ChatCompletion(APIView):
    def post(self,request,pk=None):

        user_message = request.data.get("message")
        if not user_message:
            return Response({"error": "No message provided"}, status=status.HTTP_400_BAD_REQUEST)

        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }

        headers = {
            "Authorization": f"Bearer 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",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            return Response(response.json())
        except requests.exceptions.HTTPError as http_err:
            return Response(
                {"error": str(http_err), "details": response.text},
                status=response.status_code
            )
        except Exception as e:
            return Response(
                {"error": "Something went wrong", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )