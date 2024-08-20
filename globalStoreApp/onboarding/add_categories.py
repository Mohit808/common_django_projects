

from rest_framework.views import APIView
from globalStoreApp import custom_response
from globalStoreApp.custom_response import customError, customResponse
from globalStoreApp.my_serializers import StoreSerializer, SellerSerializer
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from globalStoreApp.models import Store,Seller


class AddCategoriesFunction(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        service_type = request.data.get('service_type')
        categories = request.data.get('categories')

        ser = StoreSerializer(data={
            "service_type":service_type,
            "categories":categories
        }, context={'request': request},partial=True)

        if ser.is_valid():
            ser.save()
            return customResponse(message="Categories added sucessfully", status=status.HTTP_200_OK)
        else:
            return customResponse(message=f"{customError(ser.errors)}", status=status.HTTP_400_BAD_REQUEST)
        
