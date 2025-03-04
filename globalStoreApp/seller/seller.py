from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from globalStoreApp.models import *
from globalStoreApp.my_serializers import *
from globalStoreApp.custom_response import *
from django.db.models import Sum
from datetime import timedelta
from django.utils import timezone




@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SellerDashboard(APIView):

    def get(self,request,pk=None):
        available_items=Product.objects.filter(store=request.user.id).count()
        sold_items=Order.objects.filter(store=request.user.id,status=3).count()
        ongoing_orders = Order.objects.filter(store=request.user.id, status__in=[0, 1, 2]).count()
        total_revenue=Order.objects.filter(store=request.user.id,status=3).aggregate(Sum('discountedTotalAmount'))['discountedTotalAmount__sum']

        now = timezone.now()
        start_of_current_week = now - timedelta(days=now.weekday())
        end_of_current_week = start_of_current_week + timedelta(days=7)

        # Get the start of the previous week and end of the previous week
        start_of_previous_week = start_of_current_week - timedelta(days=7)
        end_of_previous_week = start_of_previous_week + timedelta(days=7)

        orders_this_week = Order.objects.filter(created_at__gte=start_of_current_week, created_at__lt=end_of_current_week).count()

        orders_previous_week = Order.objects.filter(created_at__gte=start_of_previous_week, created_at__lt=end_of_previous_week).count()

        if orders_previous_week > 0:
            percentage_change = ((orders_this_week - orders_previous_week) / orders_previous_week) * 100
        else:
            percentage_change = 0.0

        print(f"Orders this week: {orders_this_week}")
        print(f"Orders previous week: {orders_previous_week}")
        print(f"Percentage change: {percentage_change}%")
        
        #Average order revenue
        total_revenue_previous_week = Order.objects.filter(created_at__gte=start_of_previous_week,created_at__lt=end_of_previous_week).aggregate(Sum('discountedTotalAmount'))['discountedTotalAmount__sum']
        total_orders_previous_week = Order.objects.filter(created_at__gte=start_of_previous_week,created_at__lt=end_of_previous_week).count()
        if total_orders_previous_week > 0:
            average_order_revenue = total_revenue_previous_week / total_orders_previous_week
        else:
            average_order_revenue = 0 
        
        return customResponse(message="Data fetched successfully", status=200, data={"available_items": available_items, "sold_items": sold_items, "ongoing_orders": ongoing_orders,"total_revenue":total_revenue,"orders_this_week":orders_this_week,"orders_previous_week":orders_previous_week,"percentage_change":percentage_change,"average_order_revenue":average_order_revenue})
