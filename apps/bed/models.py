from apps.common.models import *
from apps.meta.models import *
from apps.property.models import *
from apps.room.models import *

# Bed model
class Bed(BaseModel):

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    bed_number = models.PositiveIntegerField(null=True, blank=True, default=1, unique=True)
    price_per_bed = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    is_occupied = models.BooleanField(**COMMON_NULLABLE_FIELD_CONFIG)

    def __str__(self) -> str:
        return f"Bed {self.bed_number} in {self.room}"


# Bed image model
class BedImage(FileOnlyModel):
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE, related_name="images")
    bed_image = models.ImageField(upload_to='img/', null=True)