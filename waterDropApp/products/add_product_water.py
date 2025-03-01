from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from globalStoreApp.custom_response import *
from waterDropApp.serializers_water import ProductWaterSerializer
from waterDropApp.models import UserWater, ProductWater
from rest_framework.pagination import PageNumberPagination




class CreateProduct(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ProductWaterSerializer(data=request.data,context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.validated_data['userId'] = UserWater.objects.get(email=request.user.username)
            serializer.save()
            return customResponse(message= 'Product created successfully', status=status.HTTP_200_OK)
        return customResponse(message= 'Invalid data', status=400  ,data=serializer.data)


class GetMyProduct(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request,pk=None):

        if pk:
            try:
                product = ProductWater.objects.get(id=pk)
                serializer = ProductWaterSerializer(product, context={'request': request})
                return customResponse(message= 'Fetch data successfully', status=200  ,data=serializer.data)
            except ProductWater.DoesNotExist:
                return customResponse(message= 'Product not found', status=status.HTTP_404_NOT_FOUND  )
        
        query=UserWater.objects.get(email=request.user.username)
        querySet=ProductWater.objects.filter(userId=query)
        paginator = PageNumberPagination()
        paginated_products = paginator.paginate_queryset(querySet, request)
        serializer = ProductWaterSerializer(paginated_products,context={'request': request}, many=True)
        
        return customResponse(message= 'Fetch data successfully', status=200  ,data=paginator.get_paginated_response(serializer.data).data)
    
    
    def delete(self, request,pk=None):
        print(pk)
        if pk:
            querySet=ProductWater.objects.filter(id=pk)
            querySet.delete()
            return customResponse(message= 'Delete data successfully', status=200  ,data=None)
        return customResponse(message= 'Id Not Provided', status=400  ,data=None)
    





class GetAllProduct(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request,pk=None):

        querySet=ProductWater.objects.all()
        paginator = PageNumberPagination()
        paginated_products = paginator.paginate_queryset(querySet, request)
        serializer = ProductWaterSerializer(paginated_products,context={'request': request}, many=True)
        
        return customResponse(message= 'Fetch data successfully', status=200  ,data=paginator.get_paginated_response(serializer.data).data)
    