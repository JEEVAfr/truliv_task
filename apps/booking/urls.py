from .models import *
from .serializers import *
from .views import *
from django.urls import path

API_URL_PREFIX = "api/"


urlpatterns = [

    # booking and payment url
    path(f"{API_URL_PREFIX}booking/", CreateBookingAPIView.as_view()),
    #path(f"{API_URL_PREFIX}payment/<int:booking_id>/", CreatePaymentAPIView.as_view()),
    path(f"{API_URL_PREFIX}create-razorpay-order/<int:booking_id>/", CreateRazorpayOrderAPIView.as_view()),
    path(f"{API_URL_PREFIX}confirm-razorpay-payment/<int:booking_id>/", ConfirmRazorpayPaymentAPIView.as_view()), 
]