from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import *
from rest_framework import status
from apps.common.views.base import *
from django.utils.http import urlsafe_base64_decode
from rest_framework.authtoken.models import Token
from django.conf import settings
from apps.common.views.base import *
from apps.access.serializers import *
from rest_framework.pagination import PageNumberPagination
from apps.property.views import *


# change password
class ChangePasswordView(AppAPIView, APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return self.send_response(
                data={"message": "Password updated successfully."},
                status_code=status.HTTP_200_OK,
            )
        return self.send_error_response(data={"errors": serializer.errors})

class LoginAPIView(NonAuthenticatedAPIMixin,AppAPIView, APIView):
     def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)

            response_data = {
                "email": user.email,
                "token": token.key,
            }
            return self.send_response(response_data)
        else:
            return self.send_error_response(serializer.errors)        
        

class LogoutAPIView(AppAPIView, APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()

        response_data = {
            "status": "Success",
            "detail": "Successfully logged out."
        }

        # Use the serializer to format the response
        serializer = LogoutSerializer(data=response_data)
        if serializer.is_valid():
            return self.send_response(serializer.validated_data)
        return self.send_error_response(serializer.errors)
    
class SignUpAPIView(AppAPIView, APIView):
   
   permission_classes = [IsAuthenticated] 

   def get(self, request):

        users = User.objects.all()  
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)

   
   def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return self.send_response({"message": "User created successfully", "user": serializer.data})
        return self.send_error_response(serializer.errors)


class UserProfileAPIView(NonAuthenticatedAPIMixin , AppAPIView, APIView):

    def get(self, request):
        user_profiles = UserProfile.objects.all()
        paginator = AppPagination()
        paginated_profiles = paginator.paginate_queryset(user_profiles, request)

        serializer = UserProfileSerializers(paginated_profiles, many=True)
        return paginator.get_paginated_response({
            "status": "success", 
            "data": serializer.data
        })

    def post(self, request):
        serializer = UserProfileSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.send_response({
                "data": serializer.data
            })
        return self.send_error_response({
            "errors": serializer.errors
        })