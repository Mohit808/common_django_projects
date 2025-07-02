from django.contrib import admin
from .models import *
from social_network.models import *
from dating.models import UserModel,DatingUser,LikeDating,Match,Standout,SponsoredOuting,Gift


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
admin.site.register(Transaction)
admin.site.register(Wallet)
admin.site.register(WithdrawRequest)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follow)
admin.site.register(UserModel)
admin.site.register(DatingUser)
admin.site.register(LikeDating)
admin.site.register(Match)
admin.site.register(Standout)
admin.site.register(SponsoredOuting)
admin.site.register(Gift)

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