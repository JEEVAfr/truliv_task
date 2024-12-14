from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from django.contrib.auth import views as auth_views
router = DefaultRouter()

API_URL_PREFIX = "api/"

urlpatterns = [

    # get all the user
    path(f"{API_URL_PREFIX}get-all-user/", SignUpAPIView.as_view()),
    
    # login api
    path(f"{API_URL_PREFIX}login/", LoginAPIView.as_view()),

    # log out
    path(f"{API_URL_PREFIX}log-out/", LogoutAPIView.as_view()),

    # sign up
    path(f"{API_URL_PREFIX}sign-up/", SignUpAPIView.as_view()),

    # change password
    path(f"{API_URL_PREFIX}change-password/", ChangePasswordView.as_view()),

    # user profile
    path(f"{API_URL_PREFIX}user-profile/", UserProfileAPIView.as_view()),
]