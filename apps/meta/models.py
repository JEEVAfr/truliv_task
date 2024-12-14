from apps.common.models.base import *


class Location(BaseModel):
    """location model"""

    location_name = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)

    def __str__(self) -> str:
        return self.location_name



class Amenity(BaseModel):
    """amenity model"""

    amenity_name = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)
    is_common = models.BooleanField(**COMMON_NULLABLE_FIELD_CONFIG)

    def __str__(self) -> str:
        return self.amenity_name