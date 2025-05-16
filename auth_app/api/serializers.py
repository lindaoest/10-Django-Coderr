from rest_framework import serializers
from ..models import BusinessProfile, CustomerProfile
from django.contrib.auth.models import User

class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']

    # Verify that the provided password is correct
    def validate(self, data):
        pw = data['password']
        repeated_pw = data['repeated_password']

        if pw != repeated_pw:
            raise serializers.ValidationError({'error': 'Passwörter stimmen nicht überein'})
        return data

    # Check if the email already exists
    def validate_email(self, value):
        if User.objects.filter(email=value):
            raise serializers.ValidationError({'error': 'Diese Email existiert bereits'})
        return value

    # Save User
    def create(self, validated_data):
        user = User(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()

        # Save the profile based on its type: 'customer' or 'business'
        if validated_data['type'] == 'customer':
            CustomerProfile.objects.create(user=user, type=validated_data['type'], username=validated_data['username'], email=validated_data['email'])

        if validated_data['type'] == 'business':
            BusinessProfile.objects.create(user=user, type=validated_data['type'], username=validated_data['username'], email=validated_data['email'])

        return user

class BusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location', 'tel', 'email', 'description', 'working_hours', 'created_at', 'type']

class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'email', 'uploaded_at', 'created_at', 'type']