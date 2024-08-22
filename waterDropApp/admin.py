from django.contrib import admin

from .models import UserWater,ProductWater, OrderWater

admin.site.register(UserWater)
admin.site.register(ProductWater)
admin.site.register(OrderWater)
