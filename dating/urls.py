from django.urls import path
from django.conf.urls import include
from dating.views import *



urlpatterns = [
    
    path('hello', Hello.as_view()),
    path('register', DatingRegisterView.as_view()),
    path('login', DatingLoginView.as_view()),
    path('onboarding', Onboarding.as_view()),
    path('home', Home.as_view()),
    path('like', Like.as_view()),
    # path('add-business-detail', add_business_detail.AddBusinessDetailFunction.as_view()),
    # path('add-categories', add_categories.AddCategoriesFunction.as_view()),
]
