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
from django.db.models import Sum




@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class PostBanner(APIView):
    def post(self,request):
        data=request.data.copy() 
        data['store']=request.user.id
        id = data.get('id')  
        if id:
            banner=Banner.objects.get(id=id,store=request.user.id)
            serializer = BannerSerializer(banner, data=data, partial=True)
            if(serializer.is_valid()):
                serializer.save()
                return customResponse(message='Banner updated successfully', status=200)
            else:  
                return customResponse(message=f"{serializer.errors}", status=400)
        serializer=BannerSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return customResponse(message='Banner Created sucessfully', status=200, data=serializer.data)
        return customResponse(message=f"{serializer.errors}", status=400)
    

class GetBanner(APIView):
    def get(self,request):
        storeId=request.GET.get("storeId")
        if storeId:
            query_set=Banner.objects.filter(store=storeId).order_by('-priority')
        else:
            query_set=Banner.objects.all()
        
        serializer=BannerSerializer(query_set,many=True,context={'request': request})
        return customResponse(message='Banner Fetched sucessfully', status=200, data=serializer.data)


@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class GetMyBanner(APIView):
    def get(self,request):
        query_set=Banner.objects.filter(store=request.user.id).order_by('-priority')
        serializer=BannerSerializer(query_set,many=True,context={'request': request})
        return customResponse(message='Banner Fetched sucessfully', status=200, data=serializer.data)
    

class DeleteBanner(APIView):
    def get(self,request):
        bannerId=request.GET.get("bannerId")
        if not bannerId:
            return customResponse(message="bannerId required",status=400)
        
        try:
            Banner.objects.filter(id=bannerId).delete() #not deleting data
        except Banner.DoesNotExist:
            return customResponse(message="Banner not found",status=400)
        
        return customResponse(message="Banner deleted successfully",status=200)