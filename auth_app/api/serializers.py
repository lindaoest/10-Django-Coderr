from rest_framework import serializers
from ..models import User

class RegistrationSerializer(serializers.ModelSerializer):

    repeated_password = serializers.CharField(write_only=True)
    type = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

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
        account = User(username=self.validated_data['username'], email=self.validated_data['email'], type=self.validated_data['type'])
        account.set_password(self.validated_data['password'])
        account.save()
        return account