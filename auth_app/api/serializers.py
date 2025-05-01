from rest_framework import serializers
from ..models import UserProfile, BusinessProfile, CustomerProfile
from django.contrib.auth.models import User

class RegistrationSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'repeated_password', 'type']

    def validate(self, data):
        pw = data['password']
        repeated_pw = data['repeated_password']

        if pw != repeated_pw:
            raise serializers.ValidationError({'error': 'Passwords do not match'})
        return data

    def validate_email(self, value):
        if User.objects.filter(email=value):
            raise serializers.ValidationError({'error': 'Email already exists'})
        return value

    def save(self):
        user = User(username=self.validated_data['username'], email=self.validated_data['email'])
        user.set_password(self.validated_data['password'])
        user.save()
        account = UserProfile(user=user, type=self.validated_data['type'])
        account.save()

        if self.validated_data['type'] == 'customer':
            customer = CustomerProfile(user=user, type=self.validated_data['type'], username=self.validated_data['username'], email=self.validated_data['email'])
            customer.save()

        if self.validated_data['type'] == 'business':
            business = BusinessProfile(user=user, type=self.validated_data['type'], username=self.validated_data['username'], email=self.validated_data['email'])
            business.save()

        return account

class BusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        fields = '__all__'

class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = '__all__'