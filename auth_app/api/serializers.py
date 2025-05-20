from rest_framework import serializers
from ..models import BusinessProfile, CustomerProfile
from django.contrib.auth.models import User

""" Serializer for user registration """
class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True) # Username is required
    email = serializers.EmailField(required=True) # Email is required
    password = serializers.CharField(write_only=True, required=True) # Password is write-only to avoid exposure in responses
    repeated_password = serializers.CharField(write_only=True) # Repeat password to confirm correctness
    type = serializers.CharField() # Profile type: 'customer' or 'business'

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']

    # Validate that password and repeated password match
    def validate(self, data):
        pw = data['password']
        repeated_pw = data['repeated_password']

        if pw != repeated_pw:
            raise serializers.ValidationError({'error': 'Passwörter stimmen nicht überein'})
        return data

    # Validate that the email does not already exist in the database
    def validate_email(self, value):
        if User.objects.filter(email=value):
            raise serializers.ValidationError({'error': 'Diese Email existiert bereits'})
        return value

    # Create a new user and associated profile based on profile type
    def create(self, validated_data):
        user = User(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password']) # Hash the password before saving
        user.save()

        # Create related profile depending on the 'type' field
        if validated_data['type'] == 'customer':
            CustomerProfile.objects.create(user=user, type=validated_data['type'], username=validated_data['username'], email=validated_data['email'])

        if validated_data['type'] == 'business':
            BusinessProfile.objects.create(user=user, type=validated_data['type'], username=validated_data['username'], email=validated_data['email'])

        return user

""" Serializer for the BusinessProfile model """
class BusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location', 'tel', 'email', 'description', 'working_hours', 'created_at', 'type']
        extra_kwargs = {
            'created_at': {'format': "%Y-%m-%dT%H:%M:%SZ"}
        }

""" Serializer for the CustomerProfile model """
class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'email', 'uploaded_at', 'created_at', 'type']
        extra_kwargs = {
            'created_at': {'format': "%Y-%m-%dT%H:%M:%SZ"},
            'uploaded_at': {'format': "%Y-%m-%dT%H:%M:%SZ"},
        }