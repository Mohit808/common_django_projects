from django.contrib import admin
from .models import OtpModel, Seller, Store, Category ,Brand, Tags , Product, MainCategory, Variant, FeatureListModel

admin.site.register(OtpModel)
admin.site.register(Seller)
admin.site.register(Store)
admin.site.register(MainCategory)
admin.site.register(Category)
admin.site.register(Variant)
admin.site.register(Brand)
admin.site.register(Tags)
admin.site.register(Product)
admin.site.register(FeatureListModel)