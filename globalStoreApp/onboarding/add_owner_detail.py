

from rest_framework.views import APIView
from globalStoreApp import custom_response
from globalStoreApp.custom_response import customError, customResponse
from globalStoreApp.my_serializers import StoreSerializer, SellerSerializer
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from globalStoreApp.models import Store,Seller


class AddOwnerDetailFunction(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        whatsapp_number = request.data.get('whatsapp_number')
        ser = SellerSerializer(data={
            "first_name":first_name,
            "last_name":last_name,
            "whatsapp_number":whatsapp_number
            },context={'request': request},partial=True)

        if ser.is_valid():
            ser.save()
            return customResponse(message="Add store sucessfully", status=status.HTTP_200_OK)
        else:
            return customResponse(message=f"{customError(ser.errors)}", status=status.HTTP_400_BAD_REQUEST)
        
