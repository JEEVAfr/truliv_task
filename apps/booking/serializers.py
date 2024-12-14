from apps.room.serializers import *
from apps.access.serializers import *
from rest_framework import serializers
from .models import *
from apps.room.serializers import *
from apps.access.serializers import *


class BookingSerializer(serializers.ModelSerializer):
    user = UserProfileSerializers(read_only=True)
    room = RoomSerializers(read_only=True)
    
    class Meta:
        model = Booking
        fields = ['user', 'room', 'check_in_date', 'check_out_date', 'total_price', 'payment_status']

class PaymentSerializer(serializers.ModelSerializer):
    booking = BookingSerializer(read_only=True)
    class Meta:
        model = Payment
        fields = ['booking', 'amount', 'payment_status', 'transaction_id']


class InvoiceSerializer(serializers.ModelSerializer):
    booking_id = serializers.IntegerField(source='booking.id', read_only=True)

    class Meta:
        model = Invoice
        fields = ['booking_id', 'amount', 'full_months', 'remaining_days', 'status', 'issued_date']