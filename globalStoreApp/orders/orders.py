from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.views import APIView
from globalStoreApp.custom_response import *
from globalStoreApp.models import MainCategory,Category, FeatureListModel, Address, Banner
from globalStoreApp.my_serializers import *
from django.db.models import F, FloatField, ExpressionWrapper
import random
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated


@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class GetOrders(APIView):
    def get(self,request,pk=None):
        status=request.GET.get("status")
        if not status:
            return customResponse(message="status is required",status=400)

        isCustomer=request.GET.get("isCustomer")
        if isCustomer:
            print("IsCustomer")
            querySet=Order.objects.filter(customer=request.user.id,status=status)

        isDelivery=request.GET.get("isDelivery")
        if isDelivery:
            querySet=Order.objects.filter(deliveryPartner_id=request.user.id,status=status)

        isStore=request.GET.get("isStore")
        if isStore:
            querySet=Order.objects.filter(store=request.user.id,status=status)

        if not isCustomer and not isDelivery and not isStore:
            querySet = Order.objects.filter(status=status).exclude(deliveryPartner=request.user.id)
            print("qwertyu")
        serializer=OrderSerializer(querySet,many=True,context={'request': request})
        return customResponse(message='Order Fetched sucessfully', status=200, data=serializer.data)
    

@authentication_classes([TokenAuthentication])
class GetDeliveryOrders(APIView):
    def get(self,request,pk=None):
        order_queryset = Order.objects.exclude(deliveryPartner=request.user.id)
        serializer = DeliveryOderSerializer(order_queryset, many=True,context={'request': request})
        return customResponse(message="Orders fetched successfully",status=200,data=serializer.data)
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class GetMyDeliveryOrders(APIView):
    def get(self,request,pk=None):
        status=request.GET.get("status")
        if not status:
            return customResponse(message="status is required",status=400)
        order_queryset = Order.objects.filter(deliveryPartner_id=request.user.id,status=status)
        serializer = DeliveryOderSerializer(order_queryset, many=True,context={'request': request})
        return customResponse(message="Orders fetched successfully",status=200,data=serializer.data)


@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class GetSellerOrders(APIView):
     def get(self,request,pk=None):
        status=request.GET.get("status")
        if not status:
            return customResponse(message="status is required",status=400)
        order_queryset = Order.objects.filter(store=request.user.id,status=status)
        serializer = OrderSerializer(order_queryset, many=True,context={'request': request})
        return customResponse(message="Orders fetched successfully",status=200,data=serializer.data)