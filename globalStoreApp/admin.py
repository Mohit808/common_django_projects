from django.contrib import admin
from .models import OtpModel, Seller, Store, Category ,Brand, Tags , Product, MainCategory, Variant, FeatureListModel, Order, OrderItem, Customer, Address, Banner, FestivalOffer, DeliveryPartner 

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
# admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Banner)
admin.site.register(FestivalOffer)
admin.site.register(Order)
admin.site.register(DeliveryPartner)

# class OrderAdmin(admin.ModelAdmin):
#     def formfield_for_manytomany(self, db_field, request, **kwargs):
#         if db_field.name == "orderItem":
#             if request._obj_ is not None:
#                 # Limit to the items already selected in the Order
#                 kwargs["queryset"] = request._obj_.orderItem.all()
#             else:
#                 # Show none if it's a new Order (optional)
#                 kwargs["queryset"] = OrderItem.objects.none()
#         return super().formfield_for_manytomany(db_field, request, **kwargs)

#     def get_form(self, request, obj=None, **kwargs):
#         # Store the object reference in the request
#         request._obj_ = obj
#         return super(OrderAdmin, self).get_form(request, obj, **kwargs)

# admin.site.register(Order, OrderAdmin)