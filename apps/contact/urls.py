from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

API_URL_PREFIX = "api/"

urlpatterns = [

    # contact url
    path(f"{API_URL_PREFIX}contact-us/", ContactAPIView.as_view()),

]