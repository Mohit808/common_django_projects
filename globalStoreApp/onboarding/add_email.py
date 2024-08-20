
from rest_framework.views import APIView
from globalStoreApp import custom_response
from globalStoreApp.custom_response import customResponse
from globalStoreApp.my_serializers import SellerSerializer
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from globalStoreApp.models import Seller


class AddEmailFunction(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        email = request.data.get('email')
        if email is not None:
            user=request.user
            try:
                seller_instance = Seller.objects.get(username=user.username)
            except Seller.DoesNotExist:
                return custom_response(message="Seller not found", status_code=status.HTTP_404_NOT_FOUND)
        
            ser=SellerSerializer(seller_instance,data={"email": email}, partial=True)
            if ser.is_valid():
                ser.save()
                return customResponse(message="email added successfully", status=status.HTTP_200_OK)
            return customResponse(message="Invalid email", status=status.HTTP_400_BAD_REQUEST)
        return customResponse(message="email required", status=status.HTTP_400_BAD_REQUEST)
