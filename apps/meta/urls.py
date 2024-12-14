from .models import *
from .serializers import *
from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

API_URL_PREFIX = "api/"

urlpatterns = [

    # location
    path(f"{API_URL_PREFIX}location/", LocationListCreateAPIView.as_view()),
    path(f"{API_URL_PREFIX}location/<int:id>/", LocationDetailAPIView.as_view()),

    # amenity
    path(f"{API_URL_PREFIX}amenity/", AmenityListCreateAPIView.as_view()),
    path(f"{API_URL_PREFIX}amenity/<int:id>/", AmenityDetailAPIView.as_view()),

]