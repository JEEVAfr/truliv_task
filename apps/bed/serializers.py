from .models import *
from rest_framework import serializers
from apps.meta.models import *
from apps.property.models import *
from apps.room.models import *

# bed serializers
class BedSerializers(serializers.ModelSerializer):

    # foriegn key room
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(),write_only=True)

    class Meta:

        model = Bed
        fields = ['room', 'bed_number', 'price_per_bed', 'is_occupied']

# BedImage serializers

class BedImageSerializers(serializers.ModelSerializer):
    bed = serializers.PrimaryKeyRelatedField(queryset=Bed.objects.all(), write_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = BedImage
        fields = ['bed', 'image']

    def get_image(self, obj):
        if obj.bed_image:
            return f"{settings.SITE_URL}{obj.bed_image.url}"
        return None