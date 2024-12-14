from .models import *
from .serializers import *
from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

API_URL_PREFIX = "api/"

urlpatterns = [

    # bed
    path(f"{API_URL_PREFIX}bed/", BedListCreateAPIView.as_view()),
    path(f"{API_URL_PREFIX}bed/<int:id>/", BedDetailAPIView.as_view()),

    # bed image
    path(f"{API_URL_PREFIX}bed-image/", BedImageListCreateAPIView.as_view()),
    path(f"{API_URL_PREFIX}bed-image/<int:id>/", BedImageDetailAPIView.as_view()),

]