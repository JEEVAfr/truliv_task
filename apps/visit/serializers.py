from .models import *
from rest_framework import serializers
import re

# phone number validations
def validate_phone_number(value):
    if not re.match(r'^\+?[1-9]\d{1,14}$', value):
        raise serializers.ValidationError("Invalid phone number format.")
    return value

# schedule a visit serializers
class ScheduleVisitSerializer(serializers.ModelSerializer):

    phone_number = serializers.CharField(validators=[validate_phone_number])

    class Meta:
        model = ScheduleVisit
        fields = ['property_id', 'first_name', 'last_name', 'phone_number','email', 
                  'type_sharing', 'occupation','gender', 'scheduled_date', 'scheduled_time']