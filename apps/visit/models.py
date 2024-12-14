from django.db import models
from apps.common.models.base import *
from apps.property.models import *
from apps.common.choices import *


# model schedule a visit it like a form
class ScheduleVisit(BaseModel):

    property_id = models.ForeignKey(Property, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH, blank=True, null=True)
    last_name = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH, blank=True, null=True)
    email = models.EmailField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH, null=True, blank=True)
    phone_number = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)
    occupation = models.CharField(max_length=20, null=True, blank=True, choices=OCCUPATION)
    type_sharing = models.CharField(max_length=20, null=True, blank=True, choices=ROOM_CHOICE)
    gender = models.CharField(max_length=20, null=True, blank=False, choices=GENDER_CHOICES)
    scheduled_date = models.DateField(max_length=255, null=True, blank=True)
    scheduled_time = models.TimeField(max_length=255, null=True, blank=True)