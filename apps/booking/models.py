from django.db import models
from apps.room.models import *
from apps.access.models.user import *
from apps.common.choices import *

class Booking(models.Model):

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    check_in_date = models.DateField(auto_now_add=True)
    check_out_date = models.DateField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')

class Payment(BaseModel):
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return f"Payment for Booking {self.booking.id} - {self.payment_status}"

    def generate_transaction_id(self):
        """Generate a random alphanumeric string for transaction ID."""
        import random
        import string
        transaction_id = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        return transaction_id

class Invoice(BaseModel):

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  
    full_months = models.IntegerField(default=0)  
    remaining_days = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=CHOICE, default='unpaid')
    issued_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.id} for Booking {self.booking.id}"