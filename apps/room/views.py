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


class RoomListCreateAPIView(AppAPIView):

    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["property", "occupancy_type"]
    search_fields = ["room_number"]
    ordering_fields = ["price_per_room"]

    def get(self, request):
        room = Room.objects.all()

        for backend in self.filter_backends:
            room = backend().filter_queryset(request, room, self)

        paginator = AppPagination()
        paginated_property = paginator.paginate_queryset(room, request)

        serializer = RoomSerializers(paginated_property, many=True)
        return paginator.get_paginated_response({
            "status": "success",
            "data": serializer.data
        })

    def post(self, request):
        serializer = RoomSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.send_response({
                "data": serializer.data
            })
        return self.send_error_response({
            "errors": serializer.errors
        })

class RoomDetailAPIView(AppAPIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        room = get_object_or_404(Room, id=id)
        serializer = RoomSerializers(room)
        return self.send_response({
            "data": serializer.data
        })

    def patch(self, request, id):
        room = get_object_or_404(Room, id=id)
        serializer = RoomSerializers(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.send_response({
                "data": serializer.data
            })
        return self.send_error_response({
            "errors": serializer.errors
        })

    def delete(self, request, id):
        room = get_object_or_404(Room, id=id)
        room.delete()
        return self.send_response({
            "message": "Room deleted successfully."
        })

class RoomImageListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        room_images = RoomImage.objects.all()
        serializer = RoomImageSerializers(room_images, many=True)

        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RoomImageSerializers(data=request.data)

        if serializer.is_valid():
            serializer.save()

            # Get the image URL from the serializer
            image_url = request.build_absolute_uri(serializer.data.get('image'))

            return Response({
                "status": "success",
                "data": serializer.data,
                "image_url": image_url
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class RoomImageDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):

        room_image = get_object_or_404(RoomImage, id=id)
        serializer = RoomImageSerializers(room_image)

        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def patch(self, request, id):

        room_image = get_object_or_404(RoomImage, id=id)
        serializer = RoomImageSerializers(instance=room_image, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):

        room_image = get_object_or_404(RoomImage, id=id)
        room_image.delete()

        return Response({
            "status": "success",
            "message": "Room Image deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)