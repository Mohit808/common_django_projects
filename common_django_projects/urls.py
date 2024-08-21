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
from globalStoreApp.views import index
from globalStoreApp.auth import login_view
from globalStoreApp.onboarding import add_email, add_store_name, add_owner_detail, add_business_detail,add_categories,add_address
from waterDropApp.auth import login_view as water_login
from waterDropApp.products import add_product


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

    path('social-login', water_login.LoginView.as_view()),
    path('updateUserWater', water_login.UpdateUser.as_view()),
    path('createProductWater', add_product.CreateProduct.as_view()),
    path('getProduct', add_product.GetProduct.as_view()),
]
