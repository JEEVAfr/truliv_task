from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.core.mail import EmailMessage
from apps.common.views.base import *
from apps.access.views import *

# only post method
class ContactAPIView(NonAuthenticatedAPIMixin,AppAPIView):

    def post(self, request):
        # asking data from the request
        name = request.data.get('name')
        email = request.data.get('email')
        title = request.data.get('title')
        message = request.data.get('message')

        # enter all the fields if not it will throw error
        if not all([name, email, title, message]):
            return self.send_error_response(
                {"message": "All fields (name, email, title, message) are required."})

        try:
            # send the mail
            email_message = EmailMessage(
                subject=f'Contact Form Submission: {title}',
                body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                from_email=email,
                to=['jeevakumar.jee2003@gmail.com'],
            )
            email_message.send()

            return self.send_response({"message": "Mail sent successfully"})
        except Exception as e:
            return self.send_error_response({"message": f"Mail not sent. Error: {str(e)}"})