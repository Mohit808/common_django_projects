"""
URL configuration for common_django_projects project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from globalStoreApp.views import index,GetMainCategories,GetCategory,GetProducts, GetVariants, GetDashboard, GetHotDeals, CreateOrders, GetOrders, MyAddress, GetBanner, GetStore, GetUniqueCategoryByStore, GetBrands, GetFestivalOffer, GetVariantByFestival, GetDeliveryOrders  
from globalStoreApp.auth import login_view
from globalStoreApp.onboarding import add_email, add_store_name, add_owner_detail, add_business_detail,add_categories,add_address
from waterDropApp.auth import login_view as water_login
from waterDropApp.products import add_product_water, order_water
from shareWheel.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),    
    path('',index),
    path('api-auth/', include('rest_framework.urls')),
    
    path('send-otp', login_view.LoginView.as_view()),
    path('verify-otp', login_view.VerifyOTPView.as_view()),
    path('add-email', add_email.AddEmailFunction.as_view()),
    path('add-store-name', add_store_name.AddStoreNameFunction.as_view()),
    path('add-owner-detail', add_owner_detail.AddOwnerDetailFunction.as_view()),
    path('add-business-detail', add_business_detail.AddBusinessDetailFunction.as_view()),
    path('add-categories', add_categories.AddCategoriesFunction.as_view()),
    path('add-address', add_address.AddAddressFunction.as_view()),
    path('getMainCategories', GetMainCategories.as_view()),
    path('getCategory/<int:pk>', GetCategory.as_view()),
    path('getProducts', GetProducts.as_view()),
    path('getDashboard', GetDashboard.as_view()),
    path('getVariants/<int:pk>', GetVariants.as_view()),
    path('getHotDeals', GetHotDeals.as_view()),
    path('createOrders', CreateOrders.as_view()),
    path('getOrders', GetOrders.as_view()),
    path('myAddress', MyAddress.as_view()),
    path('getBanner', GetBanner.as_view()),
    path('getStore', GetStore.as_view()),
    path('getUniqueCategoryByStore', GetUniqueCategoryByStore.as_view()),
    path('getBrands', GetBrands.as_view()),
    path('getFestivalOffer', GetFestivalOffer.as_view()),
    path('getVariantByFestival', GetVariantByFestival.as_view()),
    path('getDeliveryOrders', GetDeliveryOrders.as_view()),
    # path('getNearByAddress', GetNearByAddress.as_view()),

    path('social-login', water_login.LoginView.as_view()),
    path('updateUserWater', water_login.UpdateUser.as_view()),
    path('createProductWater', add_product_water.CreateProduct.as_view()),
    path('getMyProductWater', add_product_water.GetMyProduct.as_view()),
    path('getMyProductWater/<int:pk>', add_product_water.GetMyProduct.as_view()),
    path('getAllProduct', add_product_water.GetAllProduct.as_view()),
    path('getOrderSellerWater', order_water.GetOrderSeller.as_view()),
    path('getOrderCustomer', order_water.GetOrderCustomer.as_view()),
    path('orderNowWater', order_water.OrderNowWater.as_view()),
    path('updateOrderWater', order_water.UpdateOrderWater.as_view()),

    #share wheels
    path('wheelBookings', WheelBookingFunction.as_view()),
]

# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
