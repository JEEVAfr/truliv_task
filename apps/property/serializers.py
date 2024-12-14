from .models import *
from apps.meta.models import *
from apps.meta.serializers import *
from rest_framework import serializers
from django.conf import settings

# property serializers
class PropertySerializers(serializers.ModelSerializer):

    # location is foriegn key, amenity many to many
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(),write_only=True)
    amenities = AmenitySerializers(many=True, read_only=True)

    class Meta:

        model = Property
        fields = ['property_name', 'type_of_property', 'price_per_month', 'gender', 'rating_review',
                    'title', 'description','amenities', 'location',  'occupancy_1_price', 'occupancy_2_price',
                    'occupancy_3_price' , 'occupancy_4_price']
        
class PropertyImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    property = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all(), write_only=True)

    class Meta:
        model = PropertyImage
        fields = ('property', 'image_url')

    def get_image_url(self, obj):
        if obj.image:
            return settings.SITE_URL + obj.image.url
        return None
# property rating serializers
class PropertyRatingSerializers(serializers.ModelSerializer):

    property = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all(),write_only=True)

    class Meta:

        model = PropertyRating
        fields = ['property', 'house_service_rating', 'amenity_service_rating', 'staff_service_rating', 'opinion']

