from .models import *
from .serializers import *
from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

API_URL_PREFIX = "api/"

urlpatterns = [

    # room
    path(f"{API_URL_PREFIX}room/", RoomListCreateAPIView.as_view()),
    path(f"{API_URL_PREFIX}room/<int:id>/", RoomDetailAPIView.as_view()),

    # room image
    path(f"{API_URL_PREFIX}room-image/", RoomImageListCreateAPIView.as_view()),
    path(f"{API_URL_PREFIX}room-image/<int:id>/", RoomImageDetailAPIView.as_view()),

]