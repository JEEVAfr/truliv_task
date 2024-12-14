from .models import *
from .serializers import *
from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

API_URL_PREFIX = "api/"


urlpatterns = [

    # property
    path(f"{API_URL_PREFIX}property/", PropertyListCreateAPIView.as_view()),
    path(f"{API_URL_PREFIX}property/<int:id>/", PropertyDetailAPIView.as_view()),

    # property-web detail view
    path(f"{API_URL_PREFIX}property-web/<int:id>/", PropertyWebDetailView.as_view()),
    # property image
    path(f"{API_URL_PREFIX}property-image/", PropertyImageListCreateAPIView.as_view(), name='property-image-create'),
    path(f"{API_URL_PREFIX}property-image/<int:id>/", PropertyImageDetailAPIView.as_view()),

    # property rating
    path(f"{API_URL_PREFIX}property-rating/", PropertyRatingListCreateAPIView.as_view()),
    path(f"{API_URL_PREFIX}property-rating/<int:id>/", PropertyRatingDetailAPIView.as_view()),

]