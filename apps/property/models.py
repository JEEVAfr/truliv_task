from apps.common.models.base import *
from apps.meta.models import *
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.common.choices import *

# Property model
class Property(BaseModel):

    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    amenities = models.ManyToManyField(Amenity)
    property_name = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)
    type_of_property = models.CharField(max_length=20, null=False, blank=False, choices=PROPERTY_CHOICES)
    price_per_month = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=False, choices=GENDER_CHOICES)
    rating_review = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)
    description = models.TextField(**COMMON_NULLABLE_FIELD_CONFIG)
    occupancy_1_price = models.FloatField(max_length=20, null=True, blank=True)
    occupancy_2_price = models.FloatField(max_length=20, null=True, blank=True, default=0)
    occupancy_3_price = models.FloatField(max_length=20, null=True, blank=True, default=0)
    occupancy_4_price = models.FloatField(max_length=20, null=True, blank=True, default=0)

    def __str__(self) -> str:
        return self.property_name

class PropertyImage(FileOnlyModel):
    
    property = models.ForeignKey(Property, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='img/', null=True)
    
# Property rating model
class PropertyRating(BaseModel):

    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    house_service_rating = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    amenity_service_rating = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    staff_service_rating = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    opinion = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"Rating for {self.property.property_name}"