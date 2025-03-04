from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from globalStoreApp.models import *
from globalStoreApp.my_serializers import *
from globalStoreApp.custom_response import *
from django.db.models import Sum, Q
from datetime import timedelta
from django.utils import timezone
from django.db.models.functions import Coalesce
from django.db.models.functions import TruncDate



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
        

        seven_days_ago = timezone.now() - timedelta(days=7)
        orders_last_7_days = Order.objects.filter(created_at__gte=seven_days_ago)
        total_revenue_last_7_days = orders_last_7_days.aggregate(total_revenue=Sum(Coalesce('discountedTotalAmount', 'totalAmount')))['total_revenue']
        total_orders_last_7_days = orders_last_7_days.count()
        if total_revenue_last_7_days is None:
            total_revenue_last_7_days = 0
        
        if total_orders_last_7_days > 0:
            average_order_revenue_last_7_days = total_revenue_last_7_days / total_orders_last_7_days
        else:
            average_order_revenue_last_7_days = 0
        
        


        # last 7 day transaction
        today = timezone.now().date()
        last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
        days_of_week = [day.strftime('%a') for day in last_7_days]
        transactions_last_7_days = Transaction.objects.filter(created_at__gte=last_7_days[-1])
        total_per_day = (transactions_last_7_days.annotate(date=TruncDate('created_at')) .values('date').annotate(total_credit=Sum('amount', filter=Q(type=0)), total_debit=Sum('amount', filter=Q(type=1)) ).order_by('date'))
        result = [{'day': day_name, 'credit': 0, 'debit': 0} for day_name in days_of_week]
        for entry in total_per_day:
            day_of_week = entry['date']
            day_index = last_7_days.index(day_of_week)
            day_name = days_of_week[day_index]
            # result[day_index] = {
            #     'day': day_name,
            #     'credit': entry['total_credit'] or 0,
            #     'debit': entry['total_debit'] or 0
            #     }
        return customResponse(message="Data fetched successfully", status=200, data={"available_items": available_items, "sold_items": sold_items, "ongoing_orders": ongoing_orders,"total_revenue":total_revenue,"orders_this_week":orders_this_week,"orders_previous_week":orders_previous_week,"percentage_change":percentage_change,"average_order_revenue":average_order_revenue_last_7_days,"transaction_insights":result})
