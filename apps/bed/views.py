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

class BedListCreateAPIView(AppAPIView):

    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["room"]
    search_fields = ["bed_number"]
    ordering_fields = ["price_per_bed"]

    def get(self, request):
        bed = Bed.objects.all()

        for backend in self.filter_backends:
            bed = backend().filter_queryset(request, bed, self)

        paginator = AppPagination()
        paginated_bed = paginator.paginate_queryset(bed, request)
        serializer = BedSerializers(paginated_bed, many=True)
        return paginator.get_paginated_response({
            "status": "success",
            "data": serializer.data
        })

    def post(self, request):
        serializer = BedSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.send_response({
                "data": serializer.data
            })
        return self.send_error_response({
            "errors": serializer.errors
        })

class BedDetailAPIView(AppAPIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        bed = get_object_or_404(Bed, id=id)
        serializer = BedSerializers(bed)
        return self.send_response({
            "data": serializer.data
        })

    def patch(self, request, id):
        bed = get_object_or_404(Bed, id=id)
        serializer = BedSerializers(bed, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.send_response({
                "data": serializer.data
            })
        return self.send_error_response({
            "errors": serializer.errors
        })

    def delete(self, request, id):
        bed = get_object_or_404(Bed, id=id)
        bed.delete()
        return self.send_response({
            "message": "Bed deleted successfully."
        })

class BedImageListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        bed_images = BedImage.objects.all()
        serializer = BedImageSerializers(bed_images, many=True)

        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BedImageSerializers(data=request.data)

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

class BedImageDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):

        bed_image = get_object_or_404(BedImage, id=id)
        serializer = BedImageSerializers(bed_image)

        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def patch(self, request, id):

        bed_image = get_object_or_404(BedImage, id=id)
        serializer = BedImageSerializers(instance=bed_image, data=request.data, partial=True)

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

        bed_image = get_object_or_404(BedImage, id=id)
        bed_image.delete()

        return Response({
            "status": "success",
            "message": "Bed Image deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)