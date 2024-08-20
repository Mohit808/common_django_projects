

from rest_framework.views import APIView
from globalStoreApp import custom_response
from globalStoreApp.custom_response import customError, customResponse
from globalStoreApp.my_serializers import StoreSerializer, SellerSerializer
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from globalStoreApp.models import Store,Seller


class AddBusinessDetailFunction(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        pan_number = request.data.get('pan_number')
        gst_number = request.data.get('gst_number')
        business_name = request.data.get('business_name')


        ser = StoreSerializer(data={
            "pan_number":pan_number,
            "gst_number":gst_number,
            "business_name":business_name,

        },context={'request': request},partial=True)

        if ser.is_valid():
            ser.save()
            return customResponse(message="Business detail added sucessfully", status=status.HTTP_200_OK)
        else:
            return customResponse(message=f"{customError(ser.errors)}", status=status.HTTP_400_BAD_REQUEST)
        
