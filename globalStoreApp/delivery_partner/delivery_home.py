from datetime import date, timedelta
from django.utils.timezone import now
from globalStoreApp.models import *
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from globalStoreApp.custom_response import *
from rest_framework.views import APIView
from django.db.models import Q


@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])

class GetTodayAndWeeklyDeliveries(APIView):
    def get(self, request):
        today = date.today()
        seven_days_ago = timezone.now().date() - timedelta(days=6)
        today_deliveries = Order.objects.filter(updated_at=today,status=3,deliveryPartner=request.user.id).only('id').count()
        last_7_days_deliveries = Order.objects.filter(updated_at__date__range=[seven_days_ago, timezone.now().date()],status=3,deliveryPartner=request.user.id).only('id').count()

        percentChange=0
        percent=0
        if last_7_days_deliveries > 0:
            percentChange=(today_deliveries-last_7_days_deliveries)/last_7_days_deliveries*100
            percent=(today_deliveries-percentChange)/percentChange*100

        
        order_count = Order.objects.filter(Q(status=1) | Q(status=2),deliveryPartner=request.user.id).only('id').count()
    
        return customResponse(status=200,message="Data Fetched successfully",data={
            "today_deliveries": today_deliveries,
            "weekly_deliveries": last_7_days_deliveries,
            "percentChange": percentChange,
            "relativeGrowth": percent,
            "order_count": order_count
        })
    