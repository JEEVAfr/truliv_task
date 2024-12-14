from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.permissions import *
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.common.views.base import *

# pagination
class AppPagination(PageNumberPagination):
    page_size = 10


class LocationListCreateAPIView(AppAPIView):

    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["location_name"]
    search_fields = ["location_name"]

    def get(self, request):
        location = Location.objects.all()

        for backend in self.filter_backends:
            location = backend().filter_queryset(request, location, self)

        paginator = AppPagination()
        paginated_location = paginator.paginate_queryset(location, request)
        serializer = LocationSerializers(paginated_location, many=True)
        return paginator.get_paginated_response({
            "status": "success",
            "data": serializer.data
        })

    def post(self, request):
        serializer = LocationSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.send_response(data={"data": serializer.data})
        return self.send_error_response(data={"errors": serializer.errors})

class LocationDetailAPIView(AppAPIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        location = get_object_or_404(Location, id=id)
        serializer = LocationSerializers(location)
        return self.send_response({
            "data": serializer.data
        })

    def patch(self, request, id):
        location = get_object_or_404(Location, id=id)
        serializer = LocationSerializers(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.send_response({
                "data": serializer.data
            })
        return self.send_error_response({
            "errors": serializer.errors
        })

    def delete(self, request, id):
        location = get_object_or_404(Location, id=id)
        location.delete()
        return self.send_response({
            "message": "Location deleted successfully."
        })

class AmenityListCreateAPIView(AppAPIView):

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        amenity = Amenity.objects.all()
        paginator = AppPagination()
        paginated_amenity = paginator.paginate_queryset(amenity, request)
        serializer = AmenitySerializers(paginated_amenity, many=True)
        return paginator.get_paginated_response({
            "status": "success",
            "data": serializer.data
        })

    def post(self, request):
        serializer = AmenitySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.send_response({
                "data": serializer.data
            })
        return self.send_error_response({
            "errors": serializer.errors
        })

class AmenityDetailAPIView(AppAPIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        amenity = get_object_or_404(Amenity, id=id)
        serializer = AmenitySerializers(amenity)
        return self.send_response({
            "data": serializer.data
        })

    def patch(self, request, id):
        amenity = get_object_or_404(Amenity, id=id)
        serializer = AmenitySerializers(amenity, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.send_response({
                "data": serializer.data
            })
        return self.send_error_response({
            "errors": serializer.errors
        })

    def delete(self, request, id):
        amenity = get_object_or_404(Amenity, id=id)
        amenity.delete()
        return self.send_response({
            "message": "Amenity deleted successfully."
        })