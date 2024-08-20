

from rest_framework.views import APIView
from globalStoreApp import custom_response
from globalStoreApp.custom_response import customError, customResponse
from globalStoreApp.my_serializers import StoreSerializer, SellerSerializer
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from globalStoreApp.models import Store,Seller


class AddStoreNameFunction(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        name = request.data.get('name')

        store = StoreSerializer(data={
            "store_name":name
        },context={'request': request},partial=True)

        if store.is_valid():
            store.save()
            return customResponse(message="Add store sucessfully", status=status.HTTP_200_OK)
        else:
            return customResponse(message=f"{customError(store.errors)}", status=status.HTTP_400_BAD_REQUEST)
        
