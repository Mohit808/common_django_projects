from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from globalStoreApp.custom_response import *
from waterDropApp.serializers_water import ProductWaterSerializer
from waterDropApp.models import UserWater, ProductWater



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


class GetProduct(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        query=UserWater.objects.get(email=request.user.username)
        querySet=ProductWater.objects.filter(userId=query)
        serializer = ProductWaterSerializer(querySet,context={'request': request}, many=True)
        return customResponse(message= 'Fetch data successfully', status=200  ,data=serializer.data)
    
    def delete(self, request,pk=None):
        querySet=ProductWater.objects.delete(id=pk)
        return customResponse(message= 'Delete data successfully', status=200  ,data=None)