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
from django.db.models import Value


@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class GetOrders(APIView):
    def get(self,request,pk=None):
        status=request.GET.get("status")
        isCustomer=request.GET.get("isCustomer")
        isDelivery=request.GET.get("isDelivery")
        isStore=request.GET.get("isStore")
        
        
        if not status:
            print("1")
            return customResponse(message="status is required",status=400)

        elif isCustomer:
            print("2")
            querySet=Order.objects.filter(customer=request.user.id,status=status)
            serializer=OrderSerializer(querySet,many=True,context={'request': request})
            if status != '2':
                for data in serializer.data:
                    data.pop('otp', None)

        
        elif isDelivery:
            print("3")
            if status != '0':
                querySet=Order.objects.filter(deliveryPartner_id=request.user.id,status=status)
            else:
                querySet=Order.objects.filter(status=status)
            serializer=OrderSerializer(querySet,many=True,context={'request': request})
            for data in serializer.data:
                data.pop('otp', None)


        
        elif isStore:
            print("4")
            querySet=Order.objects.filter(store=request.user.id,status=status)
            serializer=OrderSerializer(querySet,many=True,context={'request': request})
            if status != '1':
                for data in serializer.data:
                    data.pop('otp', None)

        else:
            querySet = Order.objects.filter(status=status)
            serializer=OrderSerializer(querySet,many=True,context={'request': request})
            for data in serializer.data:
                data.pop('otp', None)
            print("5")

        return customResponse(message='Order Fetched sucessfully', status=200, data=serializer.data)
    


@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class CancelOrder(APIView):
    def get(self,request,pk=None):
        id=request.GET.get("id")
        reason=request.GET.get("reason")
        isCustomer=request.GET.get("isCustomer")
        isDelivery=request.GET.get("isDelivery")
        isStore=request.GET.get("isStore")
        if not id:
            return customResponse(message="id is required",status=400)
        if not reason:
            return customResponse(message="reason is required",status=400)
        elif isCustomer:
            order=Order.objects.get(customer=request.user.id,id=id)
            order.status='101'
            order.statusName='Cancelled by Customer'
            order.cancelReason=reason
            order.save()
        elif isDelivery:
            order=Order.objects.get(deliveryPartner_id=request.user.id,id=id)
            if order.status == 1:
                order.status = 0
                order.deliveryPartner = None
            else:
                order.status='101'
                order.statusName='Cancelled by Delivery Partner'
                order.cancelReason=reason
            order.save()
        elif isStore:
            order=Order.objects.get(store=request.user.id,id=id)
            order.status='101'
            order.statusName='Cancelled by Store'
            order.cancelReason=reason
            order.save()
        else:
            return customResponse(message="No Customer or delivery or store is not defined",status=400)

        return customResponse(message='Order Cancelled sucessfully', status=200)