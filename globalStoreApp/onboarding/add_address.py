

from rest_framework.views import APIView
from globalStoreApp import custom_response
from globalStoreApp.custom_response import customError, customResponse
from globalStoreApp.my_serializers import StoreSerializer, SellerSerializer
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from globalStoreApp.models import Store,Seller


class AddAddressFunction(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        address = request.data.get('address')
        building = request.data.get('building')
        floor = request.data.get('floor')
        tower = request.data.get('tower')
        landmark = request.data.get('landmark')
        pincode = request.data.get('pincode')
        how_to_reach = request.data.get('how_to_reach')
        country = request.data.get('country')
        state=request.data.get('state')
        city=request.data.get('city')
        lat=request.data.get('lat')
        lng=request.data.get('lng')

        ser = StoreSerializer(data={
            "store_address": address,
            "store_building": building,
            "store_floor": floor,
            "store_tower": tower,
            "store_landmark": landmark,
            "pincode": pincode,
            "store_how_to_reach": how_to_reach,
            "store_country": country,
            "store_state": state,
            "store_city": city,
            "lat":lat,
            "lng":lng
        },context={'request': request},partial=True)

        if ser.is_valid():
            ser.save()
            return customResponse(message="Address added sucessfully", status=status.HTTP_200_OK)
        else:
            return customResponse(message=f"{customError(ser.errors)}", status=status.HTTP_400_BAD_REQUEST)
        
