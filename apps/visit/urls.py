from .models import *
from .serializers import *
from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

API_URL_PREFIX = "api/"

urlpatterns = [

    # form url
    path(f"{API_URL_PREFIX}schedule-visit/", ScheduleVisitCreateAPIView.as_view()),

]