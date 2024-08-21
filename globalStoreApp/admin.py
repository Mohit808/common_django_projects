from django.contrib import admin
from .models import OtpModel, Seller, Store
from waterDropApp.models import *

admin.site.register(OtpModel)
admin.site.register(Seller)
admin.site.register(Store)
# admin.site.register(UserWater)
admin.site.register(ProductWater)