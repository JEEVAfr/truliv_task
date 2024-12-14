from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model 
import re
from apps.common.views.base import *
from apps.access.models.user import *

User = get_user_model()

# password serializers
class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value
    
    def validate_new_password(self, value):
        user = self.context['request'].user
        if user.check_password(value):
            raise serializers.ValidationError("New password is same as old password.")
        
        if len(value) != 8:
            raise serializers.ValidationError("New password must be at least 8 characters long.")
        
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("New_password must contain at least one lowercase letter.")
        
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("New_Password must contain at least one uppercase letter.")
        
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("New_Password must contain at least one digit.")
        
        if not re.search(r'[^a-zA-Z0-9]', value):
            raise serializers.ValidationError("New password must contain at least one symbol.")
        return value
    
# log in serializers
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "Invalid email"})

        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Incorrect password"})

        # Add user to validated data to pass to the view
        data['user'] = user
        return data

# log out
class LogoutSerializer(serializers.Serializer):
    # The serializer can be empty or hold fields that may be required in the future
    message = serializers.CharField(read_only=True)
    
# sign up 
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')  # Removed 'username'

    def create(self, validated_data):
        """Create a new user with the provided data."""
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)  # Only passing 'email' and 'password'
        user.set_password(password)
        user.save()
        return user

class UserProfileSerializers(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['name', 'age', 'gender', 'phone_number', 'email', 'address1']