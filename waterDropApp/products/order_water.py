from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from globalStoreApp.custom_response import *
from waterDropApp.serializers_water import OrderWaterSerializer
from waterDropApp.models import UserWater, ProductWater,OrderWater
from rest_framework.pagination import PageNumberPagination

class GetOrderSeller(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request,pk=None):
        
        query=UserWater.objects.get(email=request.user.username)
        querySet=OrderWater.objects.filter(toUser=query)
        paginator = PageNumberPagination()
        paginated_products = paginator.paginate_queryset(querySet, request)
        serializer = OrderWaterSerializer(paginated_products,context={'request': request,'include_toUser':True,'include_fromUser':False,}, many=True)
        
        return customResponse(message= 'Fetch data successfully', status=200  ,data=paginator.get_paginated_response(serializer.data).data)
    
    
    def delete(self, request,pk=None):
        print(pk)
        if pk:
            querySet=OrderWater.objects.filter(id=pk)
            querySet.delete()
            return customResponse(message= 'Delete data successfully', status=200  ,data=None)
        return customResponse(message= 'Id Not Provided', status=400  ,data=None)
    

class GetOrderCustomer(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request,pk=None):
        
        query=UserWater.objects.get(email=request.user.username)
        querySet=OrderWater.objects.filter(fromUser=query)
        paginator = PageNumberPagination()
        paginated_products = paginator.paginate_queryset(querySet, request)
        serializer = OrderWaterSerializer(paginated_products,context={'include_fromUser':True,}, many=True)
        
        return customResponse(message= f'Fetch data successfully', status=200  ,data=paginator.get_paginated_response(serializer.data).data)
    
    
    def delete(self, request,pk=None):
        print(pk)
        if pk:
            querySet=OrderWater.objects.filter(id=pk)
            querySet.delete()
            return customResponse(message= 'Delete data successfully', status=200  ,data=None)
        return customResponse(message= 'Id Not Provided', status=400  ,data=None)
    


class OrderNowWater(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = OrderWaterSerializer(data=request.data,context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.validated_data['fromUser'] = UserWater.objects.get(email=request.user.username)
            serializer.save()
            return customResponse(message= 'Order placed successfully', status=status.HTTP_200_OK)
        return customResponse(message= 'Invalid data', status=400  ,data=serializer.errors)