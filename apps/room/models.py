from apps.common.models.base import *
from apps.meta.models import *
from apps.property.models import *
from apps.common.choices import *

# Room model
class Room(BaseModel):

    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    room_number = models.PositiveIntegerField(null=True, blank=True, default=1, unique=True)
    occupancy_type = models.CharField(max_length=20, null=True, blank=False, choices=OCCUPANCY_TYPE)
    price_per_room = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"Room {self.room_number} in {self.property.property_name}"
    
# Room image model
class RoomImage(FileOnlyModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="images")
    room_image = models.ImageField(upload_to='img/', null=True)