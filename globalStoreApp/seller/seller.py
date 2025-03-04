from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from globalStoreApp.models import *
from globalStoreApp.my_serializers import *
from globalStoreApp.custom_response import *
from django.db.models import Sum

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SellerDashboard(APIView):

    def get(self,request,pk=None):
        available_items=Product.objects.filter(store=request.user.id).count()
        sold_items=Order.objects.filter(store=request.user.id,status=3).count()
        ongoing_orders = Order.objects.filter(store=request.user.id, status__in=[0, 1, 2]).count()
        total_revenue=Order.objects.filter(store=request.user.id,status=3).aggregate(Sum('total_amount'))['total_amount__sum']
        return customResponse(message="Data fetched successfully", status=200, data={"available_items": available_items, "sold_items": sold_items, "ongoing_orders": ongoing_orders,"total_revenue":total_revenue})
