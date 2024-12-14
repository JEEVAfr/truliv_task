from .models import *
from rest_framework import serializers

# location serializers
class LocationSerializers(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ['location_name']


# amenity serializers
class AmenitySerializers(serializers.ModelSerializer):

    class Meta:
        model = Amenity
        fields = ['amenity_name', 'is_common']