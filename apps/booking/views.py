import uuid
from datetime import datetime
from .serializers import *
from apps.room.models import *
from .models import *
from apps.access.models.user import UserProfile
import razorpay
from django.conf import settings
from razorpay.errors import SignatureVerificationError


class CreateBookingAPIView(AppAPIView):
    """ User selects a room, system checks availability,
    If available, booking is created with a status of pending"""
    def post(self, request):
        user_id = request.data.get('user')
        room_id = request.data.get('room')
        check_in_date_str = request.data.get('check_in_date')
        check_out_date_str = request.data.get('check_out_date')

        try:
            user = UserProfile.objects.get(id=user_id)
            room = Room.objects.get(id=room_id)

            # Check if room is available
            if not room.is_available:
                return self.send_error_response({"detail": "Room is not available."})

            # Parse the check-in and check-out dates
            check_in_date = datetime.strptime(check_in_date_str, "%Y-%m-%d").date()
            check_out_date = datetime.strptime(check_out_date_str, "%Y-%m-%d").date()

            # Calculate total price based on room price per night
            if check_in_date >= check_out_date:
                return self.send_error_response({"detail": "Check-out date must be after check-in date."})

            total_days = (check_out_date - check_in_date).days

            full_month = total_days // 30
            remaining_days = total_days % 30

            # Calculate the price
            price_per_month = room.price_per_room
            total_price = (full_month * price_per_month) + (price_per_month / 30) * remaining_days

            # Create booking
            booking = Booking.objects.create(
                user=user,
                room=room,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                total_price=total_price,
                payment_status='pending'
            )

            return self.send_response(
                data={
                    "booking": BookingSerializer(booking).data
                }
            )

        except UserProfile.DoesNotExist:
            return self.send_error_response({"detail": "User not found."})

        except Room.DoesNotExist:
            return self.send_error_response({"detail": "Room not found."})

        except Exception as e:
            return self.send_error_response({"detail": str(e)})

class CreateRazorpayOrderAPIView(AppAPIView):
    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id)
            amount = int(booking.total_price * 100) 

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET))
            razorpay_order = client.order.create({
                'amount': amount,
                'currency': 'INR',
                'payment_capture': 1
            })

            # Create payment record in the database
            payment = Payment.objects.create(
                booking=booking,
                amount=booking.total_price,
                payment_status='pending',
                transaction_id=razorpay_order['id']
            )

            return self.send_response({
                "razorpay_order_id": razorpay_order['id'],
                "razorpay_amount": amount,
                "razorpay_currency": "INR",
                "payment_status": payment.payment_status
            })

        except Booking.DoesNotExist:
            return self.send_error_response({"detail": "Booking not found."})
        except Exception as e:
            return self.send_error_response({"detail": str(e)})


class ConfirmRazorpayPaymentAPIView(AppAPIView):
    def post(self, request, booking_id):

        payment_id = request.data.get('razorpay_payment_id')
        order_id = request.data.get('razorpay_order_id')
        signature = request.data.get('razorpay_signature')

        try:
            if not payment_id or not order_id or not signature:
                return self.send_error_response({"detail": "payment_id, order_id, signatur_id is missing."})

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET))

            data = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            try:
                client.utility.verify_payment_signature(data)
            except SignatureVerificationError:
                return self.send_error_response({"detail": "Payment verification failed. Invalid signature."})

            # Fetch the payment and booking details
            payment = Payment.objects.get(transaction_id=order_id)
            booking = Booking.objects.get(id=booking_id)

            if booking.payment_status != 'pending':
                return self.send_error_response({"detail": "Payment failed."})

            # Mark the payment as successful
            payment.payment_status = 'paid'
            payment.save()

            # Update the booking status to 'confirmed'
            booking.payment_status = 'paid'
            booking.status = 'confirmed'  # Mark booking as confirmed
            booking.room.is_available = False  # Room is now unavailable
            booking.room.save()
            booking.save()

            # Calculate the total days, full months, and remaining days
            total_days = (booking.check_out_date - booking.check_in_date).days
            full_months = total_days // 30
            remaining_days = total_days % 30

            # Calculate the price
            price_per_month = booking.room.price_per_room
            total_price = (full_months * price_per_month) + (price_per_month / 30) * remaining_days

            invoice = Invoice.objects.create(
                booking=booking,
                amount=total_price,
                full_months=full_months,
                remaining_days=remaining_days,
                status='paid'
            )

            # Return the payment confirmation and invoice details
            return self.send_response({
                "detail": "Payment successfully.",
                "invoice": InvoiceSerializer(invoice).data
            })

        except Payment.DoesNotExist:
            return self.send_error_response({"detail": "Payment not found."})
        except Booking.DoesNotExist:
            return self.send_error_response({"detail": "Booking not found."})
        except Exception as e:
            return self.send_error_response({"detail": str(e)})
