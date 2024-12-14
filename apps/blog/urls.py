from .models import *
from .serializers import *
from .views import *
from django.urls import path, include
from apps.access.urls import *

API_URL_PREFIX = "api/"

urlpatterns = [

    # blog
    path(f"{API_URL_PREFIX}blog/", BlogListCreateAPIView.as_view()),
    path(f"{API_URL_PREFIX}blog/<int:id>/", BlogDetailAPIView.as_view()),

] + router.urls