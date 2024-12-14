from .models import *
from .serializers import *
from apps.meta.models import *
from apps.meta.serializers import *
from apps.room.serializers import *
from apps.bed.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.permissions import *
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import RetrieveAPIView
from apps.common.views.base import *



# pagination
class AppPagination(PageNumberPagination):
    page_size = 10


class PropertyListCreateAPIView(AppAPIView, APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["property_name", "location", "type_of_property"]
    search_fields = ["property_name", "location","type_of_property"] 
    ordering_fields = ["price_per_month",]   

    def get(self, request):
        queryset = Property.objects.all()

        # Apply filters (filtering, searching, and ordering)
        for backend in self.filter_backends:
            queryset = backend().filter_queryset(request, queryset, self)

        # Apply pagination
        paginator = AppPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        # Serialize the paginated data
        serializer = PropertySerializers(paginated_queryset, many=True)

        # Return the paginated response
        return paginator.get_paginated_response({
            "status": "success",
            "data": serializer.data
        })

    def post(self, request):
        serializer = PropertySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.send_response({
                "data": serializer.data
            })
        return self.send_error_response({
            "errors": serializer.errors
        })

class PropertyDetailAPIView(AppAPIView, APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        property = get_object_or_404(Property, id=id)
        serializer = PropertySerializers(property)
        return self.send_response({
            "data": serializer.data
        })

    def patch(self, request, id):
        property = get_object_or_404(Property, id=id)
        serializer = PropertySerializers(property, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.send_response({
                "data": serializer.data
            })
        return self.send_error_response({
            "errors": serializer.errors
        })

    def delete(self, request, id):
        property = get_object_or_404(Property, id=id)
        property.delete()
        return self.send_response({
            "message": "Property deleted successfully."
        })


class PropertyImageListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        property_images = PropertyImage.objects.all()
        serializer = PropertyImageSerializer(property_images, many=True)

        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = PropertyImageSerializer(data=request.data)
    
        if serializer.is_valid():
            serializer.save()
            image_url = request.build_absolute_uri(serializer.data.get('room_image'))
        
            return Response({
            "status": "success",
            "data": serializer.data,
            "image_url": image_url
        }, status=status.HTTP_201_CREATED)
    
    # If not valid, log errors and return a response with them
        print(serializer.errors)  # Or use logging
        return Response({
        "status": "error",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


class PropertyImageDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):

        property_image = get_object_or_404(PropertyImage, id=id)
        serializer = PropertyImageSerializer(property_image)

        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def patch(self, request, id):

        property_image = get_object_or_404(PropertyImage, id=id)
        serializer = PropertyImageSerializer(instance=property_image, data=request.data, partial=True)

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

        property_image = get_object_or_404(PropertyImage, id=id)
        property_image.delete()

        return Response({
            "status": "success",
            "message": "Property Image deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)

class PropertyRatingListCreateAPIView(AppAPIView, APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        rating = PropertyRating.objects.all()
        paginator = AppPagination()
        paginated_rating = paginator.paginate_queryset(rating, request)
        serializer = PropertyRatingSerializers(paginated_rating, many=True)
        return paginator.get_paginated_response({
            "status": "success",
            "data": serializer.data
        })

    def post(self, request):
        serializer = PropertyRatingSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.send_response({
                "data": serializer.data
            })
        return self.send_error_response({
            "errors": serializer.errors
        })

class PropertyRatingDetailAPIView(AppAPIView, APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        rating = get_object_or_404(PropertyRating, id=id)
        serializer = PropertyRatingSerializers(rating)
        return self.send_response({
            "data": serializer.data
        })

    def patch(self, request, id):
        rating = get_object_or_404(PropertyRating, id=id)
        serializer = PropertyRatingSerializers(rating, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.send_response({
                "data": serializer.data
            })
        return self.send_error_response({
            "errors": serializer.errors
        })

    def delete(self, request, id):
        rating = get_object_or_404(PropertyRating, id=id)
        rating.delete()
        return self.send_response({
            "message": "Property Rating deleted successfully."
        })

# detail view for web
class PropertyWebDetailView(AppAPIView,RetrieveAPIView):
    queryset = Property.objects.all()  
    serializer_class = PropertySerializers 
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            property_data = PropertySerializers(instance).data
            amenities_data = AmenitySerializers(instance.amenities.all(), many=True).data
            images_data = PropertyImageSerializer(instance.images.all(), many=True).data
            room_images_data = RoomImageSerializers(RoomImage.objects.filter(room__property=instance), many=True).data 
            bed_images_data = BedImageSerializers(BedImage.objects.filter(bed__room__property=instance), many=True).data

            response_data = {
                "property": property_data,
                "amenities": amenities_data,
                "images": images_data,
                "rooms": room_images_data,
                "beds": bed_images_data,
            }

            return self.send_response(response_data)

        except Property.DoesNotExist:
            return self.send_error_response(
                {"error": "Property not found."})
        except Exception as e:
            return self.send_error_response(
                {"error": str(e)})