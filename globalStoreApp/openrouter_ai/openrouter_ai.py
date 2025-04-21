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
        product = request.data.get("product")
        if not user_message:
            return Response({"error": "No message provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not product:
            return Response({"error": "No product provided"}, status=status.HTTP_400_BAD_REQUEST)

        payload = {
            "model": "meta-llama/llama-4-maverick:free",
            "messages": [
                {"role": "user", "content": f"Product name - {product} required - {user_message}",},
                {"role": "system","content": "I am building a product catalog. When I give a product name and required fields like Description, Highlights, Origin, Tips, or Additional Info, respond only with the exact two-line content for each field. Do not include any introductory or closing phrases. Do not repeat the product name or mention the field name. Only provide the content for the requested fields. Keep each response clear, concise, and aligned with the product. No extra words, no explanations — just pure, direct text for copy-paste use."},
                {"role": "assistant", "content": "You are an expert store manager who know all product in the store and its descriptionm, ingredient and all detail"}
            ]
        }

        headers = {
            "Authorization": "Bearer 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",
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