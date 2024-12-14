"""
URL configuration for truliv_replicate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from apps.meta.views import *
from apps.property.views import *
from apps.room.views import *
from apps.bed.views import *
from apps.blog.views import *

from django.shortcuts import render

def payment_page(request):
    return render(request, 'payment_page.html')

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('base/', include('apps.meta.urls')),
    path('base/', include('apps.property.urls')),
    path('base/', include('apps.room.urls')),
    path('base/', include('apps.bed.urls')),
    path('base/', include('apps.blog.urls')),
    path('base/', include('apps.access.urls')),
    path('base/', include('apps.visit.urls')),
    path('base/', include('apps.contact.urls')),
    path('base/', include('apps.booking.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Static & Media Files
# ------------------------------------------------------------------------------
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)