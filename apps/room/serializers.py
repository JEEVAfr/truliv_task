from .models import *
from rest_framework import serializers
from apps.meta.models import *
from apps.property.models import *

# room serializers
class RoomSerializers(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ['property', 'room_number', 'occupancy_type', 'price_per_room', 'is_available']

class RoomImageSerializers(serializers.ModelSerializer):
    room_image = serializers.SerializerMethodField()
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), write_only=True)

    class Meta:
        model = RoomImage
        fields = ['room', 'room_image']

    def get_room_image(self, obj):
        if obj.room_image:
            return f"{settings.SITE_URL}{obj.room_image.url}"
        return None