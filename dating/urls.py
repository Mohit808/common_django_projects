from django.urls import path
from django.conf.urls import include
from dating.views import *
from dating.fcm.fcm import *
from common_function.google_signin_dating import *


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
    path('sponsoredList', SponsoredList.as_view()),
    path('gift', GiftView.as_view()),
    path('myGift', MyGiftView.as_view()),
    path('giftToSend', GiftToSend.as_view()),
    path('support', SupportView.as_view()),
    path('aiMatch', AiMatchView.as_view()),
    path('makeDot', makeDotView.as_view()),
    path('notification', DatingNotificationView.as_view()),
    path('datingGoogleLogin', DatingGoogleLoginView.as_view()),
    # path('sendNotification', SendNotification.as_view()),

    # path('add-business-detail', add_business_detail.AddBusinessDetailFunction.as_view()),
    # path('add-categories', add_categories.AddCategoriesFunction.as_view()),
]
