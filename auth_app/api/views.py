from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import RegistrationSerializer, ProfileSerializer, BusinessProfileSerializer, CustomerProfileSerializer
from rest_framework import status
from ..models import BusinessProfile, CustomerProfile
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken

class RegistrationView(APIView):
	permission_classes = [AllowAny]

	def post(self, request, *args, **kwargs):

		serializer = RegistrationSerializer(data=request.data)

		if serializer.is_valid():
			user = serializer.save()
			token, created = Token.objects.get_or_create(user=user.user)

			return Response({
				'token': token.key,
				'user_id': user.user.pk,
				'email': user.user.email,
				'username': user.user.username
			})
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(ObtainAuthToken):
	permission_classes = [AllowAny]

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data)

		if serializer.is_valid():
			user = serializer.validated_data['user']
			token, created = Token.objects.get_or_create(user=user)

			return Response({
				'token': token.key,
				'user_id': user.pk,
				'email': user.email,
				'username': user.username
			})

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(generics.RetrieveUpdateDestroyAPIView):
	queryset = User.objects.all()
	serializer_class = ProfileSerializer
	permission_classes = [AllowAny]

class ProfileBusinessView(generics.ListCreateAPIView):
	queryset = BusinessProfile.objects.all()
	serializer_class = BusinessProfileSerializer
	permission_classes = [AllowAny]

class ProfileCustomerView(generics.ListCreateAPIView):
	queryset = CustomerProfile.objects.all()
	serializer_class = CustomerProfileSerializer
	permission_classes = [AllowAny]