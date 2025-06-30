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
    path('acceptRequest', AcceptRequest.as_view()),
    path('rejectRequest', RejectRequest.as_view()),
    path('matches', Matches.as_view()),
    path('unmatch', Unmatch.as_view()),
    path('sendMessage', SendMessage.as_view()),
    path('getUserMessages', GetUserMessages.as_view()),
    path('chatListView', ChatListView.as_view()),
    path('standouts', StandoutView.as_view()),
    path('sponsored', SponsoredView.as_view()),
    # path('add-business-detail', add_business_detail.AddBusinessDetailFunction.as_view()),
    # path('add-categories', add_categories.AddCategoriesFunction.as_view()),
]
